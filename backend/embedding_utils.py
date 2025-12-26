from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

def get_similarity(skill1, skill2):
    emb1 = model.encode([skill1])
    emb2 = model.encode([skill2])
    score = cosine_similarity(emb1, emb2)[0][0]
    return score
def get_similar_skills(input_skill, skill_list, threshold=0.6):
    similar_skills = []
    input_emb = model.encode([input_skill])
    skill_embs = model.encode(skill_list)

    for skill, emb in zip(skill_list, skill_embs):
        score = cosine_similarity([input_emb[0]], [emb])[0][0]
        if score >= threshold:
            similar_skills.append(skill)

    return similar_skills