from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil

from resume_parser import extract_text_from_pdf
from skill_extractor import extract_skills
from recommender import calculate_skill_gap


# ✅ STEP 1: create app FIRST
app = FastAPI(title="AI Career Guidance API")


# ✅ STEP 2: then add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

SKILLS_PATH = "datasets/tech_skills_dataset.json"
ROLES_PATH = "datasets/career_roles.csv"


@app.post("/analyze-resume")
async def analyze_resume(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        return {"error": "Only PDF files are allowed"}

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    resume_text = extract_text_from_pdf(file_path)
    user_skills = extract_skills(resume_text, SKILLS_PATH)
    results = calculate_skill_gap(user_skills, ROLES_PATH)

    return {
        "resume": file.filename,
        "extracted_skills": user_skills,
        "top_recommendations": results[:3]
    }
