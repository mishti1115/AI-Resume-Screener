from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader
import io
import re
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

skills = [
    "python",
    "java",
    "c++",
    "c",
    "html",
    "css",
    "javascript",
    "react",
    "node.js",
    "sql",
    "mongodb",
    "machine learning",
    "deep learning",
    "git",
    "github",
    "fastapi",
    "flask"
]


def skill_found(text, skill):

    pattern = (
        r"(?<![a-zA-Z0-9+#.])"
        + re.escape(skill)
        + r"(?![a-zA-Z0-9+#.])"
    )

    return re.search(
        pattern,
        text,
        re.IGNORECASE
    ) is not None


def detect_experience(text):

    patterns = [
        r"\b\d+\+?\s*years?\s*(of)?\s*experience\b",
        r"\b\d+\+?\s*months?\s*(of)?\s*experience\b",
        r"\bsoftware engineer\b",
        r"\bsoftware developer\b",
        r"\bdeveloper\b",
        r"\bintern\b",
        r"\binternship\b",
        r"\bwork experience\b"
    ]

    found = []

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            found.append(match.group())

    return list(dict.fromkeys(found))


def detect_education(text):

    patterns = [
        r"\bb\.?tech\b",
        r"\bb\.?e\b",
        r"\bm\.?tech\b",
        r"\bmca\b",
        r"\bbca\b",
        r"\bbachelor\b",
        r"\bmaster\b",
        r"\bcomputer science\b",
        r"\binformation technology\b",
        r"\beducation\b",
        r"\bdegree\b"
    ]

    found = []

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            found.append(match.group())

    return list(dict.fromkeys(found))


def create_summary(
    text,
    found_skills,
    experience,
    education
):

    if not text.strip():

        return "No resume text could be extracted."

    summary_parts = []

    if found_skills:

        summary_parts.append(
            "The candidate has technical skills including "
            + ", ".join(found_skills)
            + "."
        )

    if experience:

        summary_parts.append(
            "The resume contains professional experience information."
        )

    if education:

        summary_parts.append(
            "Educational qualifications are also present."
        )

    if not summary_parts:

        return (
            "The resume was processed, but limited "
            "professional information was detected."
        )

    return " ".join(summary_parts)


def get_ai_analysis(
    resume_text,
    job_description
):

    prompt = f"""
You are an AI Resume Screener.

Analyze the resume against the job description.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Give a concise professional analysis using these sections:

1. Candidate Summary
2. Job Fit
3. Key Strengths
4. Missing or Weak Areas
5. Improvement Suggestions

Rules:
- Use only information present in the resume and job description.
- Do not invent experience, skills, education, or achievements.
- Keep the analysis clear and useful for the candidate.
"""
    client = genai.Client()

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


@app.get("/")
def home():

    return {
        "message": "AI Resume Screener is running"
    }


@app.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):

    content = await file.read()

    reader = PdfReader(
        io.BytesIO(content)
    )

    text = ""

    for page in reader.pages:

        extracted = page.extract_text()

        if extracted:
            text += extracted + "\n"

    found_skills = []

    for skill in skills:

        if skill_found(text, skill):

            found_skills.append(skill)

    job_skills = []

    for skill in skills:

        if skill_found(job_description, skill):

            job_skills.append(skill)

    matched_skills = []

    for skill in job_skills:

        if skill in found_skills:

            matched_skills.append(skill)

    missing_skills = []

    for skill in job_skills:

        if skill not in found_skills:

            missing_skills.append(skill)

    if job_skills:

        match_percentage = round(
            len(matched_skills)
            / len(job_skills)
            * 100
        )

    else:

        match_percentage = 0

    experience = detect_experience(text)

    education = detect_education(text)

    summary = create_summary(
        text,
        found_skills,
        experience,
        education
    )

    feedback = []

    if missing_skills:

        feedback.append(
            "Consider adding these skills to your resume: "
            + ", ".join(missing_skills)
        )

    if match_percentage < 50:

        feedback.append(
            "Your resume has a low skill match with this job description."
        )

    elif match_percentage < 80:

        feedback.append(
            "Your resume has a moderate skill match with this job description."
        )

    else:

        feedback.append(
            "Your resume has a strong skill match with this job description."
        )

    if not found_skills:

        feedback.append(
            "No technical skills were detected in the resume."
        )

    if not experience:

        feedback.append(
            "No clear work experience information was detected."
        )

    if not education:

        feedback.append(
            "No clear education information was detected."
        )

    strengths = []

    if found_skills:

        strengths.append(
            "Technical skills detected: "
            + ", ".join(found_skills)
        )

    if matched_skills:

        strengths.append(
            "Your resume matches "
            + str(len(matched_skills))
            + " required skill(s) from the job description."
        )

    if experience:

        strengths.append(
            "Experience information was detected in the resume."
        )

    if education:

        strengths.append(
            "Education information was detected in the resume."
        )

    if match_percentage >= 80:

        strengths.append(
            "Your resume has strong alignment with the job requirements."
        )

    try:

        ai_analysis = get_ai_analysis(
            text,
            job_description
        )

    except Exception as error:

        print("\n================ AI ERROR ================")
        print(error)
        print("==========================================\n")

        ai_analysis = (
            "Local AI Error: "
            + str(error)
        )

    return {

        "filename": file.filename,

        "summary": summary,

        "ai_analysis": ai_analysis,

        "resume_skills": found_skills,

        "job_skills": job_skills,

        "matched_skills": matched_skills,

        "missing_skills": missing_skills,

        "match_percentage": match_percentage,

        "experience": experience,

        "education": education,

        "feedback": feedback,

        "strengths": strengths
    }
