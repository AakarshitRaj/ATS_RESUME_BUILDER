from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.colors import black
import PyPDF2
from io import BytesIO

def preserve_resume_format(input_pdf_path, tailored_text, output_path):
    """
    Preserve original resume format and replace content with tailored text
    """
    try:
        # Read original PDF to get dimensions and layout info
        with open(input_pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            first_page = pdf_reader.pages[0]
            
            # Get page dimensions
            page_width = float(first_page.mediabox.width)
            page_height = float(first_page.mediabox.height)
        
        # Create new PDF with same dimensions
        c = canvas.Canvas(output_path, pagesize=(page_width, page_height))
        
        # Set font and margins similar to original
        margin = 0.75 * inch
        text_width = page_width - (2 * margin)
        y_position = page_height - margin
        
        # Parse tailored text and write to PDF
        lines = tailored_text.split('\n')
        
        for line in lines:
            if y_position < margin:
                c.showPage()
                y_position = page_height - margin
            
            line = line.strip()
            if not line:
                y_position -= 0.2 * inch
                continue
            
            # Detect headings (all caps or starts with common section names)
            is_heading = (line.isupper() or 
                         any(line.startswith(h) for h in ['EXPERIENCE', 'EDUCATION', 'SKILLS', 
                                                           'SUMMARY', 'PROFESSIONAL', 'WORK']))
            
            if is_heading:
                c.setFont("Helvetica-Bold", 12)
                y_position -= 0.3 * inch
            elif line.startswith('•') or line.startswith('-'):
                c.setFont("Helvetica", 10)
                line = '  ' + line
            else:
                c.setFont("Helvetica", 10)
            
            # Handle long lines
            if len(line) > 90:
                words = line.split()
                current_line = ''
                for word in words:
                    if len(current_line + word) < 90:
                        current_line += word + ' '
                    else:
                        c.drawString(margin, y_position, current_line.strip())
                        y_position -= 0.2 * inch
                        current_line = word + ' '
                if current_line:
                    c.drawString(margin, y_position, current_line.strip())
                    y_position -= 0.2 * inch
            else:
                c.drawString(margin, y_position, line)
                y_position -= 0.2 * inch
        
        c.save()
        return output_path
        
    except Exception as e:
        raise Exception(f"Error preserving format: {str(e)}")