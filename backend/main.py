from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os, shutil

from resume_parser import extract_text_from_pdf
from skill_extractor import extract_skills
from recommender import calculate_skill_gap

app = FastAPI(title="AI Career Guidance API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

SKILLS_PATH = os.path.join(BASE_DIR, "datasets", "tech_skills_dataset.json")
ROLES_PATH = os.path.join(BASE_DIR, "datasets", "career_roles.csv")


@app.post("/analyze-resume")
async def analyze_resume(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        return {"error": "Only PDF files are allowed"}

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        resume_text = extract_text_from_pdf(file_path)
        user_skills = extract_skills(resume_text, SKILLS_PATH)
        results = calculate_skill_gap(user_skills, ROLES_PATH)
    except Exception as e:
        return {"error": str(e)}

    return {
        "resume": file.filename,
        "extracted_skills": user_skills,
        "top_recommendations": results[:3]
    }
