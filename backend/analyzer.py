import spacy
import re

nlp = spacy.load("en_core_web_sm")

SKILLS_LIST = {
    "frontend": [
        "html", "css", "javascript", "react", "tailwind", "typescript",
        "redux", "next.js", "vue", "angular", "sass", "bootstrap",
        "jquery", "webpack", "vite"
    ],
    "backend": [
        "node.js", "express", "python", "java", "flask", "django",
        "rest api", "graphql", "php", "spring", "fastapi"
    ],
    "database": [
        "mongodb", "sql", "mysql", "postgresql", "firebase",
        "mongoose", "redis", "sqlite", "supabase"
    ],
    "tools": [
        "git", "github", "linux", "docker", "aws", "github actions",
        "vercel", "netlify", "postman", "ci/cd"
    ],
    "dsa": [
        "data structures", "algorithms", "leetcode", "hackerrank",
        "dynamic programming", "binary search", "graphs", "trees",
        "heaps", "sorting", "recursion"
    ]
}

ACTION_VERBS = [
    "built", "developed", "created", "designed", "implemented",
    "optimized", "managed", "led", "deployed", "improved",
    "architected", "integrated", "automated", "delivered", "launched",
    "engineered", "reduced", "increased", "scaled", "refactored",
    "contributed", "achieved"
]

WEAK_WORDS = [
    "helped", "assisted", "tried", "worked on", "familiar with",
    "exposure to", "basic knowledge", "learning", "knowledge of",
    "understanding of", "involved in"
]

IMPACT_PATTERNS = [
    r'\d+\+',
    r'top\s+\d+%',
    r'\d+(?:st|nd|rd|th)\s+place',
    r'\d+\s*(?:users|projects|apps|websites|clients)',
    r'\d+%\s*(?:faster|better|improvement|reduction|increase)',
]

SECTION_KEYWORDS = {
    "experience":     ["experience", "internship", "work", "job", "freelance"],
    "education":      ["education", "university", "college", "bca", "btech", "school", "degree"],
    "projects":       ["project", "built", "developed", "created", "app", "website", "platform"],
    "skills":         ["skill", "technologies", "tech stack", "proficient"],
    "achievements":   ["achievement", "award", "rank", "winner", "hackathon", "competition", "top"],
    "certifications": ["certification", "certified", "certificate", "course", "udemy", "coursera"],
    "contact":        ["email", "phone", "linkedin", "github", "portfolio", "gmail"],
    "summary":        ["summary", "about", "objective", "profile", "overview"]
}

def extract_skills(text):
    text_lower = text.lower()
    return {cat: [s for s in skills if s in text_lower]
            for cat, skills in SKILLS_LIST.items()}

def extract_action_verbs(text):
    text_lower = text.lower()
    return [v for v in ACTION_VERBS if v in text_lower]

def detect_weak_words(text):
    text_lower = text.lower()
    return [w for w in WEAK_WORDS if w in text_lower]

def extract_metrics(text):
    found = []
    for pattern in IMPACT_PATTERNS:
        found.extend(re.findall(pattern, text.lower()))
    return list(set(found))

def check_sections(text):
    text_lower = text.lower()
    return {sec: any(w in text_lower for w in words)
            for sec, words in SECTION_KEYWORDS.items()}

def spacy_extract(text):
    doc = nlp(text)
    return {
        "organizations": list(set(e.text for e in doc.ents if e.label_ == "ORG")),
        "dates":         list(set(e.text for e in doc.ents if e.label_ == "DATE")),
        "numbers":       list(set(e.text for e in doc.ents if e.label_ == "CARDINAL")),
    }

def count_projects(text):
    text_lower = text.lower()
    matches = re.findall(r'(project|app|platform|website|tool)\s*[\:\-\|]', text_lower)
    github_links = re.findall(r'github\.com/\S+', text_lower)
    return max(len(matches), len(github_links))

def generate_roast(score, all_skills, skills_by_cat, weak_words,
                   metrics, word_count, project_count, sections):
    roasts = []

    if score < 40:
        roasts.append("Bhai ye resume hai ya grocery list? Recruiter ne dekha hoga toh chai pine chale gaye honge!")
    elif score < 55:
        roasts.append("Resume dekh ke lagta hai tune 10 minute mein banaya — aur recruiter ne 5 second mein delete kar diya!")
    elif score < 70:
        roasts.append("Bura nahi hai bhai, but recruiter confused hai ki tu developer hai ya 'developed' karna seekh raha hai!")
    elif score < 85:
        roasts.append("Achha hai bhai! But still — LinkedIn pe Open to Work banner lagana band kar, pehle resume strong kar!")
    else:
        roasts.append("Wah bhai wah! Resume itna strong hai ki recruiter ka phone already ring ho raha hoga!")

    if len(all_skills) < 5:
        roasts.append(f"Sirf {len(all_skills)} skills? Bhai mera 10 saal ka bhatija bhi zyada skills jaanta hai!")
    if not skills_by_cat["database"]:
        roasts.append("Database skill nahi hai? Bhai data kahan store karega — Excel mein?")
    if not skills_by_cat["dsa"]:
        roasts.append("DSA mention nahi? FAANG companies ne already tera resume blacklist kar diya hoga!")
    if weak_words:
        roasts.append(f"'{', '.join(weak_words)}' likha hai resume mein? Bhai ye job application hai, confession nahi!")
    if not metrics:
        roasts.append("Koi numbers nahi hain — recruiter ko kaise pata chalega ki tune kuch kiya bhi ya bas GitHub pe star diya?")
    if word_count < 200:
        roasts.append(f"Sirf {word_count} words? Bhai meri WhatsApp status teri se zyada detailed hai!")
    elif word_count > 800:
        roasts.append(f"{word_count} words ka resume? Recruiter novel padhne nahi aaya interview mein!")
    if project_count < 2:
        roasts.append("Ek hi project hai? Bhai ek project se job milti toh sab log FAANG join kar lete!")
    if not sections["summary"]:
        roasts.append("Summary section nahi hai — recruiter ko khud guess karna padega ki tu human hai ya bot!")
    if not sections["achievements"]:
        roasts.append("Achievements section nahi? Matlab zindagi mein kuch achieve hi nahi kiya? Abhi time hai!")
    if not sections["contact"]:
        roasts.append("Contact info nahi hai — recruiter carrier pigeon bheje kya tujhe hire karne ke liye?")

    if score >= 70:
        roasts.append("Overall solid hai bhai — bas thoda polish kar, job pakki samajh!")
    else:
        roasts.append("Chal bhai himmat rakh — sabka pehla resume aisa hi hota hai. Fix kar aur wapas aa!")

    return roasts

def calculate_score(text):
    skills_by_cat = extract_skills(text)
    all_skills    = [s for cat in skills_by_cat.values() for s in cat]
    verbs         = extract_action_verbs(text)
    weak_words    = detect_weak_words(text)
    metrics       = extract_metrics(text)
    sections      = check_sections(text)
    spacy_data    = spacy_extract(text)
    word_count    = len(text.split())
    project_count = count_projects(text)

    scores = {}

    skill_score = min(24, len(all_skills) * 2)
    if skills_by_cat["frontend"] and skills_by_cat["backend"]:
        skill_score += 4
    if skills_by_cat["dsa"]:
        skill_score += 2
    scores["skills"] = min(30, skill_score)

    exp_score = 0
    if sections["experience"]:
        exp_score += 8
        exp_score += min(6, len(verbs))
        exp_score += min(4, len(metrics))
        if not weak_words:
            exp_score += 2
    scores["experience"] = min(20, exp_score)

    proj_score = 0
    if sections["projects"]:
        proj_score += 8
        proj_score += min(8, project_count * 4)
        if metrics:
            proj_score += 5
        if sections["achievements"]:
            proj_score += 4
    scores["projects"] = min(25, proj_score)

    edu_score = 0
    if sections["education"]:
        edu_score += 10
        if len(spacy_data["dates"]) >= 2:
            edu_score += 3
        if sections["certifications"]:
            edu_score += 2
    scores["education"] = min(15, edu_score)

    fmt_score = 0
    if sections["contact"]:  fmt_score += 3
    if sections["summary"]:  fmt_score += 2
    if 300 <= word_count <= 700:
        fmt_score += 5
    elif 200 <= word_count < 300:
        fmt_score += 3
    else:
        fmt_score += 1
    scores["formatting"] = min(10, fmt_score)

    total = sum(scores.values())

    feedback  = []
    strengths = []

    if len(all_skills) < 6:
        feedback.append(f"Sirf {len(all_skills)} skills detect hui — 8-10 add karo.")
    if not skills_by_cat["database"]:
        feedback.append("Database skill nahi — MongoDB ya SQL add karo.")
    if not skills_by_cat["dsa"]:
        feedback.append("DSA mention nahi — LeetCode ya data structures add karo.")
    if weak_words:
        feedback.append(f"Weak words hain: '{', '.join(weak_words)}' — strong action verbs use karo.")
    if not metrics:
        feedback.append("Measurable results nahi — '150+ users', '40% faster' jaisi cheezein add karo.")
    if project_count < 2:
        feedback.append("Kam se kam 2-3 projects add karo.")
    if not sections["achievements"]:
        feedback.append("Achievements section nahi — hackathon, rankings add karo.")
    if not sections["summary"]:
        feedback.append("Summary/About section nahi — 2-3 line ka intro add karo.")
    if not sections["contact"]:
        feedback.append("Contact info missing — email, LinkedIn, GitHub add karo.")
    if word_count < 300:
        feedback.append(f"Resume chota hai ({word_count} words) — 300-600 words ideal hai.")

    if len(all_skills) >= 8:
        strengths.append(f"Strong skill set — {len(all_skills)} technologies listed hain.")
    if skills_by_cat["frontend"] and skills_by_cat["backend"]:
        strengths.append("Full-stack profile clearly dikhti hai.")
    if skills_by_cat["dsa"]:
        strengths.append("DSA skills mentioned hain — product companies ke liye plus point.")
    if metrics:
        strengths.append(f"Measurable results hain — resume strong lagta hai.")
    if len(verbs) >= 5:
        strengths.append(f"{len(verbs)} strong action verbs use kiye hain.")
    if sections["achievements"]:
        strengths.append("Achievements section hai — recruiters ka dhyan jata hai.")
    if project_count >= 2:
        strengths.append(f"{project_count} projects detect hue — achha portfolio hai.")

    roast = generate_roast(total, all_skills, skills_by_cat, weak_words,
                           metrics, word_count, project_count, sections)

    return {
        "total_score":        total,
        "grade":              get_grade(total),
        "breakdown":          scores,
        "skills_by_category": skills_by_cat,
        "all_skills_found":   all_skills,
        "action_verbs":       verbs,
        "weak_words_found":   weak_words,
        "metrics_found":      metrics,
        "sections_present":   sections,
        "spacy_entities":     spacy_data,
        "word_count":         word_count,
        "project_count":      project_count,
        "feedback":           feedback,
        "strengths":          strengths,
        "roast":              roast,
        "job_matches": match_job_roles(all_skills),
    }

def get_grade(score):
    if score >= 85: return "A - Excellent"
    if score >= 70: return "B - Good"
    if score >= 55: return "C - Average"
    return "D - Needs Work"
JOB_ROLES = {
    "Frontend Developer": {
        "must": ["html", "css", "javascript", "react"],
        "good": ["typescript", "tailwind", "redux", "next.js", "vue"],
        "bonus": ["figma", "webpack", "vite"]
    },
    "Backend Developer": {
        "must": ["node.js", "python", "express"],
        "good": ["sql", "mongodb", "rest api", "flask", "django"],
        "bonus": ["docker", "aws", "graphql", "redis"]
    },
    "Full Stack Developer": {
        "must": ["html", "css", "javascript", "react", "node.js"],
        "good": ["mongodb", "sql", "express", "tailwind"],
        "bonus": ["docker", "aws", "typescript", "graphql"]
    },
    "Data Structures Engineer": {
        "must": ["leetcode", "algorithms", "data structures"],
        "good": ["python", "java", "graphs", "heaps", "dynamic programming"],
        "bonus": ["hackerrank", "binary search", "recursion"]
    },
    "DevOps Engineer": {
        "must": ["git", "github", "linux", "docker"],
        "good": ["aws", "ci/cd", "github actions", "vercel"],
        "bonus": ["kubernetes", "terraform", "nginx"]
    },
    "Python Developer": {
        "must": ["python"],
        "good": ["flask", "django", "fastapi", "sql", "mongodb"],
        "bonus": ["docker", "aws", "rest api", "graphql"]
    }
}

def match_job_roles(all_skills):
    skills_set = set(all_skills)
    results = []

    for role, requirements in JOB_ROLES.items():
        must_have   = set(requirements["must"])
        good_have   = set(requirements["good"])
        bonus_have  = set(requirements["bonus"])

        must_matched  = must_have & skills_set
        good_matched  = good_have & skills_set
        bonus_matched = bonus_have & skills_set

        must_score  = (len(must_matched)  / len(must_have))  * 60
        good_score  = (len(good_matched)  / len(good_have))  * 30
        bonus_score = (len(bonus_matched) / len(bonus_have)) * 10

        total = round(must_score + good_score + bonus_score)

        missing = list((must_have | good_have) - skills_set)[:3]

        if total >= 30:
            results.append({
                "role":           role,
                "match":          total,
                "must_matched":   list(must_matched),
                "good_matched":   list(good_matched),
                "missing_skills": missing,
                "verdict": (
                    "Strong fit!"        if total >= 75 else
                    "Good fit"           if total >= 55 else
                    "Partial fit"        if total >= 35 else
                    "Skills add karo"
                )
            })

    results.sort(key=lambda x: x["match"], reverse=True)
    return results[:3]