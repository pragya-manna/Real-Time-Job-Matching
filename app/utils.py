import re

def clean_text(text):
    text = re.sub(r"\s+", " ", text)  # Remove extra whitespace
    text = re.sub(r"[^\w\s]", "", text)  # Remove punctuation
    return text.lower().strip()
def extract_skills(text, skill_list):
    found_skills = []
    for skill in skill_list:
        if skill.lower() in text.lower():
            found_skills.append(skill)
    return list(set(found_skills))
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def rank_jobs_by_similarity(user_text, job_descriptions):
    corpus = [user_text] + job_descriptions
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)
    scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    ranked_jobs = sorted(zip(job_descriptions, scores), key=lambda x: x[1], reverse=True)
    return ranked_jobs
import requests

def safe_api_call(url, payload):
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API call failed: {e}")
        return {}
