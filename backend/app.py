from resume_parser import extract_text_from_pdf
from skill_extractor import extract_skills
from recommender import calculate_skill_gap
import os
import warnings

# Suppress pdfplumber font warnings
warnings.filterwarnings("ignore", category=UserWarning)


def main():
	resume_path = "resume_k.pdf"
	skills_path = "datasets/tech_skills_dataset.json"
	roles_path = "datasets/career_roles.csv"

	if not os.path.exists(resume_path):
		print(f"Resume not found at {resume_path}. Place your resume PDF there or update the path in app.py.")
		return
	if not os.path.exists(skills_path):
		print(f"Skills dataset not found at {skills_path}.")
		return
	if not os.path.exists(roles_path):
		print(f"Roles dataset not found at {roles_path}.")
		return

	resume_text = extract_text_from_pdf(resume_path)
	user_skills = extract_skills(resume_text, skills_path)
	print(f"Extracted {len(user_skills)} skills from resume\n")
	print("Extracted skills:", user_skills)
	results = calculate_skill_gap(user_skills, roles_path)

	print("Top 3 career recommendations:")
	for i, r in enumerate(results[:3], 1):
		print(f"\n{i}. {r['role']} - {r['match_percentage']}% match")
		if r['missing_skills']:
			print(f"   Missing: {', '.join(r['missing_skills'][:3])}")


if __name__ == "__main__":
	main()
