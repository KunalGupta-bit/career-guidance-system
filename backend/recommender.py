import pandas as pd
import re


def _split_skills(raw):
    parts = re.split(r"\||;|,| or ", str(raw))
    return [p.strip() for p in parts if p and p.strip()]


def calculate_skill_gap(user_skills, csv_path):
    df = pd.read_csv(csv_path)
    results = []

    role_col = "role" if "role" in df.columns else ("job_role" if "job_role" in df.columns else None)
    skills_col = "required_skills" if "required_skills" in df.columns else None

    if role_col is None or skills_col is None:
        raise ValueError("CSV must contain 'role' or 'job_role' and 'required_skills' columns")

    user_skills_norm = set([s.strip().lower() for s in user_skills])

    for _, row in df.iterrows():
        role = row[role_col]
        required_raw = row[skills_col]
        required = _split_skills(required_raw)
        required_norm = list(set([r.lower() for r in required]))

        if len(required_norm) == 0:
            match = 0.0
            missing = []
        else:   
            missing_norm = [
    r for r in required_norm
    if not any(r in u or u in r for u in user_skills_norm)
]

            match = round((len(required_norm) - len(missing_norm)) / len(required_norm) * 100, 2)
            # map missing back to original casing where possible
            missing = [r for r in required if r.strip().lower() in missing_norm]

        results.append({
            "role": role,
            "match_percentage": match,
            "missing_skills": missing
        })

    return sorted(results, key=lambda x: x["match_percentage"], reverse=True)
if __name__ == "__main__":
    # Test with sample user skills and CSV file
    sample_skills = ["Python", "Machine Learning", "Data Analysis"]
    recommendations = calculate_skill_gap(sample_skills, "datasets/career_roles.csv")
    for rec in recommendations:
        print(rec)