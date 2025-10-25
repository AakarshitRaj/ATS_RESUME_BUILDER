from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from utils.pdf_parser import extract_text_from_pdf, parse_resume
from utils.resume_generator import tailor_resume_with_ai, generate_pdf_resume

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'message': 'Resume Tailor API is running'})

@app.route('/api/tailor-resume', methods=['POST'])
def tailor_resume():
    try:
        # Check if file is present
        if 'resume' not in request.files:
            return jsonify({'error': 'No resume file provided'}), 400
        
        file = request.files['resume']
        job_description = request.form.get('job_description')
        api_key = request.form.get('api_key')
        
        if not job_description:
            return jsonify({'error': 'No job description provided'}), 400
        
        if not api_key:
            return jsonify({'error': 'No API key provided. Get free key from https://makersuite.google.com/app/apikey'}), 400
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Only PDF files are allowed'}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Extract text from PDF
        resume_text = extract_text_from_pdf(filepath)
        
        if not resume_text.strip():
            return jsonify({'error': 'Could not extract text from PDF'}), 400
        
        # Tailor resume using AI (returns plain text now)
        tailored_text = tailor_resume_with_ai(resume_text, job_description, api_key)
        
        # Generate new PDF preserving format
        output_filename = f"tailored_{filename}"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        generate_pdf_resume(tailored_text, filepath, output_path)
        
        # Verify file was created
        if not os.path.exists(output_path):
            raise Exception("PDF generation failed - file not created")
        
        print(f"✅ PDF generated successfully: {output_path}")
        
        # Clean up original file
        if os.path.exists(filepath):
            os.remove(filepath)
        
        download_url = f'/api/download/{output_filename}'
        print(f"📥 Download URL: {download_url}")
        
        return jsonify({
            'success': True,
            'message': 'Resume tailored successfully',
            'download_url': download_url,
            'filename': output_filename,
            'preview': {'text': tailored_text[:500] + '...'}  # Preview first 500 chars
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        safe_filename = secure_filename(filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)
        
        # Check if file exists
        if not os.path.exists(filepath):
            return jsonify({'error': f'File not found: {safe_filename}'}), 404
        
        return send_file(
            filepath, 
            as_attachment=True, 
            download_name=safe_filename,
            mimetype='application/pdf'
        )
    except Exception as e:
        print(f"Download error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Resume Tailor API starting...")
    print("📝 Server running on http://localhost:5000")
    print("🔑 Get your free Google Gemini API key from: https://makersuite.google.com/app/apikey")
    app.run(debug=True, port=5000)