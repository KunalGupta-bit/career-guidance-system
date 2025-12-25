import json
import re

def extract_skills(resume_text, skill_file):
    with open(skill_file, "r") as f:
        data = json.load(f)
    
    # Handle nested JSON structure with "tech_skills" key
    if isinstance(data, dict) and "tech_skills" in data:
        skills = data["tech_skills"]
    else:
        skills = data if isinstance(data, list) else []

    extracted = []
    resume_lower = resume_text.lower().replace("-", " ")
    
    for skill in skills:
        skill_lower = skill.lower()
        # Use word boundary regex to match whole words, not substrings
        # This prevents "Python" from matching "Pythonic" or partial matches
        if re.search(r'\b' + re.escape(skill_lower) + r'\b', resume_lower):
            extracted.append(skill)

    return list(set(extracted))
if __name__ == "__main__":
    # Test with sample resume text and skill file
    sample_text = "Experienced in Python, Java, and machine learning."
    skills = extract_skills(sample_text.lower(), "datasets/tech_skills_dataset.json")
    print(skills)
