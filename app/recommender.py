import requests
import os

JOOBLE_API_KEY = os.getenv("JOOBLE_API_KEY")

def get_job_recommendations(keywords, location):
    payload = {
        "keywords": keywords,
        "location": location
    }
    response = requests.post(
        f"https://jooble.org/api/{JOOBLE_API_KEY}",
        json=payload
    )
    jobs = response.json().get("jobs", [])
    total_count = response.json().get("totalCount", 0)

    return jobs[:10], total_count # Return top 10 jobs
