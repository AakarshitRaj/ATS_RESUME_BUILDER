from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import google.generativeai as genai
import PyPDF2
import os

def tailor_resume_with_ai(resume_text, job_description, api_key):
    """Use Google Gemini API to tailor resume to JD"""
    try:
        genai.configure(api_key=api_key)
        # Using Gemini 2.5 Flash - Latest stable model (Oct 2025)
        model = genai.GenerativeModel('gemini-2.5-flash')
        print(f"✅ Using AI Model: gemini-2.5-flash")
        
        prompt = f"""
You are an expert ATS resume optimizer. Given the original resume and job description, rewrite the resume content to be perfectly tailored while MAINTAINING THE EXACT SAME FORMAT AND STRUCTURE.

ORIGINAL RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

CRITICAL INSTRUCTIONS:
1. Keep the EXACT SAME sections, order, and structure as the original resume
2. Keep all contact information unchanged (name, email, phone)
3. Enhance and optimize the content to match the job description keywords
4. Quantify achievements with metrics where possible
5. Use strong action verbs from the job description
6. Make it ATS-friendly by matching relevant keywords
7. DO NOT add new sections or remove existing ones
8. DO NOT change the person's actual work history or education
9. ONLY enhance the descriptions and achievements
10. Keep the same formatting style (bullets, spacing, capitalization)

OUTPUT FORMAT:
Return the tailored resume in plain text, preserving the original structure EXACTLY. Use the same section headers, bullet points, and formatting as the original.
"""
        
        response = model.generate_content(prompt)
        tailored_text = response.text
        
        # Clean up the response
        tailored_text = tailored_text.strip()
        
        # Remove any markdown code blocks if present
        if tailored_text.startswith('```'):
            lines = tailored_text.split('\n')
            tailored_text = '\n'.join(lines[1:-1])
        
        return tailored_text
            
    except Exception as e:
        raise Exception(f"AI Error: {str(e)}")

def generate_pdf_resume(tailored_text, input_pdf_path, output_path):
    """Generate a PDF resume preserving original format"""
    try:
        # Read original PDF to understand layout
        with open(input_pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            first_page = pdf_reader.pages[0]
            page_width = float(first_page.mediabox.width)
            page_height = float(first_page.mediabox.height)
        
        # Create new PDF with tailored content
        doc = SimpleDocTemplate(
            output_path, 
            pagesize=(page_width, page_height),
            topMargin=0.75*inch, 
            bottomMargin=0.75*inch,
            leftMargin=0.75*inch, 
            rightMargin=0.75*inch
        )
        
        styles = getSampleStyleSheet()
        story = []
        
        # Custom styles matching common resume formats
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=10,
            leading=14,
            spaceBefore=0,
            spaceAfter=6,
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=12,
            textColor=colors.HexColor('#000000'),
            spaceAfter=10,
            spaceBefore=12,
            fontName='Helvetica-Bold',
        )
        
        name_style = ParagraphStyle(
            'NameStyle',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#000000'),
            spaceAfter=6,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        # Parse and format the tailored text
        lines = tailored_text.split('\n')
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                story.append(Spacer(1, 0.1*inch))
                continue
            
            # Detect if it's likely the name (first non-empty line)
            if i == 0 or (i < 3 and len(line) < 50 and not '@' in line):
                story.append(Paragraph(line, name_style))
            # Detect section headings
            elif (line.isupper() or 
                  any(line.upper().startswith(h) for h in ['EXPERIENCE', 'EDUCATION', 'SKILLS', 
                                                            'SUMMARY', 'PROFESSIONAL', 'WORK', 
                                                            'OBJECTIVE', 'CERTIFICATIONS'])):
                story.append(Spacer(1, 0.15*inch))
                story.append(Paragraph(f"<b>{line}</b>", heading_style))
            # Bullet points
            elif line.startswith('•') or line.startswith('-') or line.startswith('*'):
                story.append(Paragraph(line, normal_style))
            # Regular text
            else:
                story.append(Paragraph(line, normal_style))
        
        doc.build(story)
        return output_path
        
    except Exception as e:
        raise Exception(f"PDF generation error: {str(e)}")