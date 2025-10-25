const API_URL = 'http://localhost:5000/api';

// Load saved API key
window.addEventListener('DOMContentLoaded', () => {
    const savedKey = localStorage.getItem('gemini_api_key');
    if (savedKey) {
        document.getElementById('apiKey').value = savedKey;
    }
});

// Save API key when changed
document.getElementById('apiKey').addEventListener('change', (e) => {
    localStorage.setItem('gemini_api_key', e.target.value);
});

// File upload handler
document.getElementById('resumeFile').addEventListener('change', (e) => {
    const fileName = e.target.files[0]?.name || 'Choose a PDF file';
    document.getElementById('fileName').textContent = fileName;
});

// Form submission
document.getElementById('resumeForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const apiKey = document.getElementById('apiKey').value.trim();
    const resumeFile = document.getElementById('resumeFile').files[0];
    const jobDescription = document.getElementById('jobDescription').value.trim();
    
    // Validation
    if (!apiKey) {
        showError('Please enter your Google Gemini API key');
        return;
    }
    
    if (!resumeFile) {
        showError('Please upload your resume PDF');
        return;
    }
    
    if (!jobDescription) {
        showError('Please enter the job description');
        return;
    }
    
    // Hide previous results/errors
    document.getElementById('resultSection').style.display = 'none';
    document.getElementById('errorSection').style.display = 'none';
    
    // Show loading state
    setLoading(true);
    
    try {
        // Prepare form data
        const formData = new FormData();
        formData.append('resume', resumeFile);
        formData.append('job_description', jobDescription);
        formData.append('api_key', apiKey);
        
        // Make API request
        const response = await fetch(`${API_URL}/tailor-resume`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to tailor resume');
        }
        
        // Show results
        showResults(data);
        
    } catch (error) {
        showError(error.message);
    } finally {
        setLoading(false);
    }
});

function setLoading(isLoading) {
    const submitBtn = document.getElementById('submitBtn');
    const btnText = document.getElementById('btnText');
    const btnLoader = document.getElementById('btnLoader');
    
    submitBtn.disabled = isLoading;
    btnText.style.display = isLoading ? 'none' : 'inline';
    btnLoader.style.display = isLoading ? 'inline-block' : 'none';
    
    if (isLoading) {
        btnText.textContent = 'Tailoring Resume...';
    } else {
        btnText.textContent = '✨ Tailor My Resume';
    }
}

function showResults(data) {
    const resultSection = document.getElementById('resultSection');
    const previewSection = document.getElementById('previewSection');
    
    // Build preview HTML
    let previewHTML = '';
    
    if (data.preview && data.preview.text) {
        previewHTML = `
            <div class="preview-item">
                <h4>📄 Tailored Resume Preview</h4>
                <p style="white-space: pre-wrap; font-family: monospace; background: #f8f9fa; padding: 15px; border-radius: 5px;">${data.preview.text}</p>
                <p style="color: #666; font-style: italic; margin-top: 10px;">Download the full PDF to see complete tailored resume</p>
            </div>
        `;
    }
    
    previewSection.innerHTML = previewHTML;
    
    // Set download URL
    const downloadBtn = document.getElementById('downloadBtn');
    const filename = data.download_url.split('/').pop(); // Extract just the filename
    
    downloadBtn.onclick = async () => {
        try {
            // Use correct URL format
            const downloadUrl = `${API_URL}/download/${filename}`;
            console.log('Downloading from:', downloadUrl);
            
            const response = await fetch(downloadUrl);
            if (!response.ok) {
                throw new Error(`Server returned ${response.status}`);
            }
            
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            
            console.log('✅ Download successful!');
        } catch (error) {
            console.error('Download error:', error);
            alert('Download failed: ' + error.message);
        }
    };
    
    resultSection.style.display = 'block';
    resultSection.scrollIntoView({ behavior: 'smooth' });
}

function showError(message) {
    const errorSection = document.getElementById('errorSection');
    const errorMessage = document.getElementById('errorMessage');
    
    errorMessage.textContent = message;
    errorSection.style.display = 'block';
    errorSection.scrollIntoView({ behavior: 'smooth' });
}