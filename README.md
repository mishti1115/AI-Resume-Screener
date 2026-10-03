# AI Resume Screener

An AI-powered Resume Screener that analyzes a resume against a given job description and provides a detailed job-fit analysis.

## 🚀 Live Demo

[AI Resume Screener](https://mishti1115.github.io/AI-Resume-Screener/)

## 📸 Project Screenshot

![AI Resume Screener](screenshot.jpeg)

## ✨ Features

- Upload a PDF resume
- Enter a job description
- Extract technical skills from the resume
- Compare resume skills with job requirements
- Calculate overall job match percentage
- Detect experience information
- Detect education information
- Identify matched and missing skills
- Generate AI-powered resume analysis
- Provide improvement suggestions
- Display resume strengths and feedback

## 🛠️ Technologies Used

### Frontend
- HTML
- CSS
- JavaScript

### Backend
- Python
- FastAPI
- PyPDF

### AI
- Google Gemini API

### Deployment
- GitHub Pages — Frontend
- Render — Backend

## 🏗️ Project Structure

```text
AI-Resume-Screener/
│
├── backend/
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── docs/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── screenshot.jpeg
├── README.md
└── .gitignore


🔄 How It Works
User
  ↓
Upload Resume + Job Description
  ↓
GitHub Pages Frontend
  ↓
FastAPI Backend
  ↓
PDF Text Extraction
  ↓
Skill Matching
  ↓
Google Gemini AI Analysis
  ↓
Resume Analysis Dashboard

📊 Analysis Includes
Overall Job Match Percentage
Resume Skills
Required Job Skills
Matched Skills
Missing Skills
Experience Detection
Education Detection
AI Candidate Summary
Job Fit Analysis
Key Strengths
Missing or Weak Areas
Improvement Suggestions

🔐 Note

The resume content is processed by the backend and relevant resume text is sent to the Google Gemini API for AI analysis.

👩‍💻 Author

Srishti
