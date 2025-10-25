# 🎯 AI Resume Tailor - Complete Setup Guide

A free, AI-powered application that tailors your resume to any job description for better ATS compatibility.

## 🌟 Features

- ✅ **ATS Optimized** - Matches keywords from job descriptions
- 🤖 **AI-Powered** - Uses Google Gemini AI (100% free)
- 📄 **PDF Support** - Upload and download PDF resumes
- 🎨 **Professional Output** - Clean, formatted resume PDFs
- 🔒 **Privacy First** - Everything runs locally, API key stored in browser
- 💯 **Free Forever** - No subscriptions, no hidden costs

---

## 📋 Prerequisites

1. **Python 3.8 or higher**
   - Download from: https://www.python.org/downloads/
   - ✅ Check "Add Python to PATH" during installation

2. **Google Gemini API Key (Free)**
   - Get yours at: https://makersuite.google.com/app/apikey
   - Sign in with Google account
   - Click "Create API Key"
   - Copy and save the key

---

## 🚀 Installation Steps

### Step 1: Create Project Structure

```bash
# Create main folder
mkdir resume-tailor
cd resume-tailor

# Create subfolders
mkdir backend frontend
mkdir backend/utils backend/uploads
```

### Step 2: Set Up Backend

1. **Create these files in `backend/` folder:**

   - `requirements.txt` (copy from artifact above)
   - `app.py` (copy from artifact above)

2. **Create these files in `backend/utils/` folder:**

   - `__init__.py` (create empty file)
   - `pdf_parser.py` (copy from artifact above)
   - `resume_generator.py` (copy from artifact above)

3. **Create `__init__.py`:**
   ```bash
   # On Windows:
   type nul > backend/utils/__init__.py
   
   # On Mac/Linux:
   touch backend/utils/__init__.py
   ```

4. **Install Python packages:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

   If you get permission errors, try:
   ```bash
   pip install --user -r requirements.txt
   ```

### Step 3: Set Up Frontend

Create these files in `frontend/` folder:
- `index.html` (copy from artifact above)
- `style.css` (copy from artifact above)
- `script.js` (copy from artifact above)

---

## ▶️ Running the Application

### Start Backend Server

```bash
# Navigate to backend folder
cd backend

# Run the server
python app.py
```

You should see:
```
🚀 Resume Tailor API starting...
📝 Server running on http://localhost:5000
🔑 Get your free Google Gemini API key from: https://makersuite.google.com/app/apikey
```

**Keep this terminal open!**

### Start Frontend

Open a **new terminal/command prompt**:

```bash
# Navigate to frontend folder
cd frontend

# On Windows:
start index.html

# On Mac:
open index.html

# On Linux:
xdg-open index.html
```

Or simply **double-click** `index.html` in your file explorer.

---

## 📖 How to Use

1. **Get API Key:**
   - Visit https://makersuite.google.com/app/apikey
   - Sign in with Google
   - Create API key (free, no credit card needed)

2. **Open Application:**
   - Go to http://localhost:5000 (or open index.html)
   - Paste your API key in the first field

3. **Upload Resume:**
   - Click "Choose a PDF file"
   - Select your existing resume (must be PDF)

4. **Paste Job Description:**
   - Copy the entire job posting
   - Paste into the text area

5. **Generate:**
   - Click "✨ Tailor My Resume"
   - Wait 15-30 seconds for AI processing
   - Preview and download your tailored resume

---

## 📁 Final Folder Structure

```
resume-tailor/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── pdf_parser.py
│   │   └── resume_generator.py
│   └── uploads/
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
└── README.md
```

---

## 🐛 Troubleshooting

### "Module not found" errors
```bash
pip install --upgrade -r requirements.txt
```

### "Port 5000 already in use"
Edit `app.py`, change the last line to:
```python
app.run(debug=True, port=5001)
```
Then update `script.js` to use port 5001

### "CORS error" in browser
Make sure:
1. Backend server is running
2. Frontend is accessing correct URL
3. Flask-CORS is installed

### "Invalid API key"
- Get new key from https://makersuite.google.com/app/apikey
- Make sure you copied the entire key
- Check if API is enabled in Google Cloud Console

### PDF extraction fails
- Ensure PDF has selectable text (not scanned image)
- Try converting your resume to a new PDF
- Use Adobe PDF or similar tool to recreate it

---

## 💡 Tips for Best Results

1. **Resume Quality:**
   - Use a clean, ATS-friendly resume template
   - Ensure text is selectable (not images)
   - Include clear sections (Experience, Education, Skills)

2. **Job Description:**
   - Paste the complete JD (not just URL)
   - Include requirements, responsibilities, and qualifications
   - More detail = better tailoring

3. **API Key:**
   - Free tier has daily limits (check Google's docs)
   - Create multiple keys if needed
   - Your key is stored locally in browser

---

## 🔒 Privacy & Security

- ✅ All processing happens on your computer
- ✅ API key stored only in your browser
- ✅ Files deleted after processing
- ✅ No data sent to third parties (except Google Gemini API)
- ✅ Open source - review the code yourself

---

## 🆓 Free Alternatives

This tool uses **Google Gemini API** which is free. Alternatives:

1. **OpenAI API** - Requires credit card, paid after trial
2. **Anthropic Claude** - Limited free tier
3. **Hugging Face** - Free but requires more setup

Google Gemini is recommended for beginners (truly free, no card needed).

---

## 🤝 Need Help?

1. **Check Troubleshooting section above**
2. **Verify all files are created correctly**
3. **Make sure Python and packages are installed**
4. **Check that both servers are running**

---

## 📝 License

Free to use, modify, and distribute. No warranty provided.

---

## 🎉 You're All Set!

Your resume tailor is ready to use. Happy job hunting! 🚀