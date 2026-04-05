import requests

resume = """
Chetan Prajapat - Full Stack Developer
Skills: React, Node.js, MongoDB, HTML, CSS, JavaScript, Git, GitHub
Built FitBridge fitness platform using React and Node.js for clients.
Ranked top 1% in UI hackathon. Solved 150+ DSA problems on LeetCode.
Internship at Rebenok Infotech - developed responsive web apps using HTML CSS JavaScript.
Deployed SiteReadyPro web template platform using Node.js and MongoDB.
BCA from Sage University Indore 2024-2027.
Email: chetanprajapat340@gmail.com LinkedIn GitHub Portfolio
"""

r = requests.post(
    "http://127.0.0.1:5000/analyze",
    json={"text": resume},
    headers={"Content-Type": "application/json"}
)

data = r.json()

print("=" * 40)
print(f"TOTAL SCORE : {data['total_score']} / 100")
print(f"GRADE       : {data['grade']}")
print("=" * 40)
print("\nBREAKDOWN:")
for k, v in data["breakdown"].items():
    print(f"  {k:15} : {v}")
print("\nSKILLS FOUND:")
for cat, skills in data["skills_by_category"].items():
    print(f"  {cat:15} : {skills}")
print(f"\nMETRICS     : {data['metrics_found']}")
print(f"WEAK WORDS  : {data['weak_words_found']}")
print(f"WORD COUNT  : {data['word_count']}")
print("\nFEEDBACK:")
for f in data["feedback"]:
    print(f"  - {f}")
print("\nSTRENGTHS:")
for s in data["strengths"]:
    print(f"  + {s}")