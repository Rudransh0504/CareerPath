from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from docx import Document
import fitz  # PyMuPDF
import re

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Common resume keywords
RESUME_KEYWORDS = [
    "education", "experience", "skills", "projects", "certifications",
    "achievements", "internship", "training", "objective", "summary",
    "contact", "email", "phone", "linkedin", "github"
]

def extract_text_from_pdf(file):
    file.file.seek(0)
    doc = fitz.open(stream=file.file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_docx(file):
    file.file.seek(0)
    doc = Document(file.file)
    return " ".join([p.text for p in doc.paragraphs])

def ats_score(resume_text, job_desc=""):
    resume_text = resume_text.lower()
    
    # Job description match
    job_score = 0
    if job_desc:
        job_keywords = set(re.findall(r'\b\w+\b', job_desc.lower()))
        resume_words = set(re.findall(r'\b\w+\b', resume_text))
        match_jd = job_keywords & resume_words
        if job_keywords:
            job_score = (len(match_jd) / len(job_keywords)) * 100
    else:
        match_jd = []

    # Resume quality match
    found_keywords = [kw for kw in RESUME_KEYWORDS if kw in resume_text]
    resume_score = (len(found_keywords) / len(RESUME_KEYWORDS)) * 100

    # Combine
    final_score = round((job_score * 0.7 + resume_score * 0.3) if job_desc else resume_score, 2)

    return final_score, found_keywords

@app.post("/ats-check")
async def ats_check(resume: UploadFile, job_desc: str = Form("")):
    try:
        resume.file.seek(0)
        if resume.filename.endswith(".pdf"):
            resume_text = extract_text_from_pdf(resume)
        elif resume.filename.endswith(".docx"):
            resume_text = extract_text_from_docx(resume)
        else:
            return {"error": "Unsupported file type"}

        score, keywords = ats_score(resume_text, job_desc)
        return {"score": score, "keywords": keywords}

    except Exception as e:
        return {"error": str(e)}
