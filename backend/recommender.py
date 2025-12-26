import pandas as pd
import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load model ONCE (important for performance)
model = SentenceTransformer("all-MiniLM-L6-v2")

SIMILARITY_THRESHOLD = 0.65


def _split_skills(raw):
    parts = re.split(r"\||;|,| or ", str(raw))
    return [p.strip() for p in parts if p and p.strip()]


def _is_similar(skill_a, skill_b):
    """
    Returns True if two skills are semantically similar
    """
    emb = model.encode([skill_a, skill_b])
    score = cosine_similarity([emb[0]], [emb[1]])[0][0]
    return score >= SIMILARITY_THRESHOLD


def calculate_skill_gap(user_skills, csv_path):
    df = pd.read_csv(csv_path)
    results = []

    role_col = "role" if "role" in df.columns else ("job_role" if "job_role" in df.columns else None)
    skills_col = "required_skills" if "required_skills" in df.columns else None

    if role_col is None or skills_col is None:
        raise ValueError("CSV must contain 'role' and 'required_skills' columns")

    user_skills_clean = [u.strip().lower() for u in user_skills]

    for _, row in df.iterrows():
        role = row[role_col]
        required = _split_skills(row[skills_col])

        matched = []
        missing = []

        for req in required:
            req_lower = req.lower()
            found = False

            for user_skill in user_skills_clean:
                if _is_similar(req_lower, user_skill):
                    found = True
                    matched.append(req)
                    break

            if not found:
                missing.append(req)

        if len(required) == 0:
            match_percentage = 0.0
        else:
            match_percentage = round((len(matched) / len(required)) * 100, 2)

        results.append({
            "role": role,
            "match_percentage": match_percentage,
            "missing_skills": missing
        })

    return sorted(results, key=lambda x: x["match_percentage"], reverse=True)


if __name__ == "__main__":
    sample_skills = [
        "Python",
        "Data Visualization",
        "Leadership",
        "Communication"
    ]

    recs = calculate_skill_gap(sample_skills, "datasets/career_roles_extended.csv")
    for r in recs[:3]:
        print(r)
    print("\nTop 3 Recommendations:")
    for rec in recs[:3]:
        print(f"Role: {rec['role']}, Match: {rec['match_percentage']}%, Missing Skills: {rec['missing_skills']}")