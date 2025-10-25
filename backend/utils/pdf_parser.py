import PyPDF2
import re

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF resume"""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        raise Exception(f"Error reading PDF: {str(e)}")

def parse_resume(text):
    """Parse resume text into structured data"""
    resume_data = {
        'name': '',
        'email': '',
        'phone': '',
        'skills': [],
        'experience': [],
        'education': [],
        'full_text': text
    }
    
    # Extract email
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    if emails:
        resume_data['email'] = emails[0]
    
    # Extract phone
    phone_pattern = r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]'
    phones = re.findall(phone_pattern, text)
    if phones:
        resume_data['phone'] = phones[0]
    
    # Extract name (first non-empty line usually)
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    if lines:
        resume_data['name'] = lines[0]
    
    return resume_data