from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client["resumexpert"]
collection = db["analyses"]

def save_analysis(analysis_id, resume_text, result):
    try:
        collection.insert_one({
            "id":           analysis_id,
            "resume_text":  resume_text[:500],
            "score":        result["total_score"],
            "grade":        result["grade"],
            "skills":       result["all_skills_found"],
            "feedback":     result["feedback"],
            "job_matches":  result.get("job_matches", []),
            "created_at":   datetime.now().strftime("%d %b %Y, %I:%M %p")
        })
    except Exception as e:
        print(f"DB save error: {e}")

def get_history():
    try:
        records = list(collection.find(
            {}, {"_id": 0}
        ).sort("created_at", -1).limit(10))
        return records
    except Exception as e:
        print(f"DB fetch error: {e}")
        return []