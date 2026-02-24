from flask import render_template, request
from app import app
from app.recommender import get_job_recommendations
from datetime import datetime
import re
import html

def format_updated_date(raw_date):
    try:
        dt = datetime.fromisoformat(raw_date)
        return dt.strftime('%d %B %Y')  # e.g., "23 August 2025"
    except ValueError:
        return "Unknown"

def clean_snippet(raw_snippet):
    unescaped = html.unescape(raw_snippet)
    cleaned = re.sub(r'<[^>]+>', '', unescaped)
    return cleaned.strip()
def compute_match_score(job, skills, location):
    score = 0
    total_weight = 0

    # Normalize inputs
    skills = [s.strip().lower() for s in skills.split(",")]
    location = location.lower()

    # Skills match
    if 'snippet' in job:
        snippet = job['snippet'].lower()
        skill_matches = sum(1 for skill in skills if skill in snippet)
        score += skill_matches * 2  # weight for skills
        total_weight += len(skills) * 2


    # Location match
    if 'location' in job and location:
        if location in job['location'].lower():
            score += 2
        total_weight += 2

    # Normalize score
    return round(score / total_weight, 2) if total_weight else 0

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        keywords = request.form["keywords"]
        location = request.form["location"]
        jobs, total_count = get_job_recommendations(keywords, location)

        # Clean each job's fields
        for job in jobs:
            job['updated'] = format_updated_date(job.get('updated', ''))
            job['snippet'] = clean_snippet(job.get('snippet', ''))
            job['score'] = compute_match_score(job, keywords, location)

        return render_template("results.html", jobs=jobs, total_count=total_count, keywords=keywords,location=location)
    return render_template("index.html")




