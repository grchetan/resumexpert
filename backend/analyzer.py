import spacy
import re

nlp = spacy.load("en_core_web_sm")

SKILLS_LIST = {
    "frontend": [
        "html", "css", "javascript", "react", "tailwind", "typescript",
        "redux", "next.js", "vue", "angular", "sass", "bootstrap",
        "jquery", "webpack", "vite", "figma"
    ],
    "backend": [
        "node.js", "express", "python", "java", "flask", "django",
        "rest api", "graphql", "php", "spring", "fastapi", "c++"
    ],
    "database": [
        "mongodb", "sql", "mysql", "postgresql", "firebase",
        "mongoose", "redis", "sqlite", "supabase"
    ],
    "tools": [
        "git", "github", "linux", "docker", "aws", "github actions",
        "vercel", "netlify", "postman", "jira", "figma", "ci/cd"
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
    "engineered", "reduced", "increased", "scaled", "migrated",
    "refactored", "mentored", "contributed", "published", "achieved"
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
    r'\d+\s*(?:users|projects|apps|websites|clients|stars)',
    r'\d+%\s*(?:faster|better|improvement|reduction|increase)',
    r'(?:increased|reduced|improved)\s+by\s+\d+',
]

SECTION_KEYWORDS = {
    "experience":     ["experience", "internship", "work", "job", "employment", "freelance"],
    "education":      ["education", "university", "college", "bca", "btech", "mca", "mtech", "school", "degree"],
    "projects":       ["project", "built", "developed", "created", "app", "website", "platform"],
    "skills":         ["skill", "technologies", "tech stack", "proficient", "expertise"],
    "achievements":   ["achievement", "award", "rank", "winner", "hackathon", "competition", "prize", "top"],
    "certifications": ["certification", "certified", "certificate", "course", "udemy", "coursera"],
    "contact":        ["email", "phone", "linkedin", "github", "portfolio", "gmail"],
    "summary":        ["summary", "about", "objective", "profile", "overview"]
}

def extract_skills(text):
    text_lower = text.lower()
    found = {}
    for category, skills in SKILLS_LIST.items():
        found[category] = [s for s in skills if s in text_lower]
    return found

def extract_action_verbs(text):
    text_lower = text.lower()
    return [v for v in ACTION_VERBS if v in text_lower]

def detect_weak_words(text):
    text_lower = text.lower()
    return [w for w in WEAK_WORDS if w in text_lower]

def extract_metrics(text):
    found = []
    for pattern in IMPACT_PATTERNS:
        matches = re.findall(pattern, text.lower())
        found.extend(matches)
    return list(set(found))

def check_sections(text):
    text_lower = text.lower()
    return {
        section: any(w in text_lower for w in words)
        for section, words in SECTION_KEYWORDS.items()
    }

def spacy_extract(text):
    doc = nlp(text)
    return {
        "organizations": list(set(e.text for e in doc.ents if e.label_ == "ORG")),
        "dates":         list(set(e.text for e in doc.ents if e.label_ == "DATE")),
        "numbers":       list(set(e.text for e in doc.ents if e.label_ == "CARDINAL")),
    }

def count_projects(text):
    text_lower = text.lower()
    # Project headings count karo
    matches = re.findall(
        r'(project|app|platform|website|tool|system)\s*[\:\-\|]',
        text_lower
    )
    # Aur GitHub links count karo
    github_links = re.findall(r'github\.com/\S+', text_lower)
    return max(len(matches), len(github_links))

def calculate_score(text):
    roast = generate_roast({
        "total_score": total,
        "all_skills_found": all_skills,
        "skills_by_category": skills_by_cat,
        "weak_words_found": weak_words,
        "metrics_found": metrics,
        "word_count": word_count,
        "project_count": project_count,
        "sections_present": sections,
    })
    skills_by_cat  = extract_skills(text)
    all_skills     = [s for cat in skills_by_cat.values() for s in cat]
    verbs          = extract_action_verbs(text)
    weak_words     = detect_weak_words(text)
    metrics        = extract_metrics(text)
    sections       = check_sections(text)
    spacy_data     = spacy_extract(text)
    word_count     = len(text.split())
    project_count  = count_projects(text)

    scores = {}

    # --- Skills (30 marks) ---
    skill_score = min(24, len(all_skills) * 2)
    if skills_by_cat["frontend"] and skills_by_cat["backend"]:
        skill_score += 4   # full stack bonus
    if skills_by_cat["dsa"]:
        skill_score += 2   # DSA bonus
    scores["skills"] = min(30, skill_score)

    # --- Experience (20 marks) ---
    exp_score = 0
    if sections["experience"]:
        exp_score += 8
        exp_score += min(6, len(verbs) * 1)   # action verbs
        exp_score += min(4, len(metrics))       # measurable results
        if not weak_words:
            exp_score += 2                      # no weak words bonus
    scores["experience"] = min(20, exp_score)

    # --- Projects (25 marks) ---
    proj_score = 0
    if sections["projects"]:
        proj_score += 8
        proj_score += min(8, project_count * 4)   # har project ke 4 marks
        if metrics:
            proj_score += 5                        # impact/metrics hain
        if sections["achievements"]:
            proj_score += 4                        # hackathon/ranking mention
    scores["projects"] = min(25, proj_score)

    # --- Education (15 marks) ---
    edu_score = 0
    if sections["education"]:
        edu_score += 10
        if len(spacy_data["dates"]) >= 2:
            edu_score += 3   # dates properly mentioned
        if sections["certifications"]:
            edu_score += 2   # certifications hain
    scores["education"] = min(15, edu_score)

    # --- Formatting (10 marks) ---
    fmt_score = 0
    if sections["contact"]:   fmt_score += 3
    if sections["summary"]:   fmt_score += 2
    if 300 <= word_count <= 700:
        fmt_score += 5
    elif 200 <= word_count < 300:
        fmt_score += 3
    elif word_count < 200:
        fmt_score += 1
    scores["formatting"] = min(10, fmt_score)

    total = sum(scores.values())

    # --- Smart Feedback ---
    feedback  = []
    strengths = []

    # Skills feedback
    if len(all_skills) < 6:
        feedback.append(f"Sirf {len(all_skills)} skills detect hui — kam se kam 8-10 add karo.")
    if not skills_by_cat["database"]:
        feedback.append("Koi database skill nahi — MongoDB ya SQL zaroor add karo.")
    if not skills_by_cat["tools"]:
        feedback.append("Tools mention nahi — Git, GitHub, Postman add karo.")
    if not skills_by_cat["dsa"]:
        feedback.append("DSA mention nahi — LeetCode problems ya data structures add karo.")

    # Experience feedback
    if weak_words:
        feedback.append(f"Weak words hain: '{', '.join(weak_words)}' — strong action verbs use karo.")
    if len(verbs) < 4:
        feedback.append("Action verbs kam hain — 'built', 'deployed', 'optimized' jaisi words use karo.")

    # Projects feedback
    if not metrics:
        feedback.append("Koi measurable result nahi — '150+ users', 'top 1%', '40% faster' jaisi cheezein add karo.")
    if project_count < 2:
        feedback.append("Sirf 1 project dikh raha hai — kam se kam 2-3 projects add karo.")
    if not sections["achievements"]:
        feedback.append("Achievements section nahi — hackathon results, rankings, awards add karo.")

    # Formatting feedback
    if not sections["summary"]:
        feedback.append("Summary/About section nahi — 2-3 line ka professional summary add karo.")
    if not sections["contact"]:
        feedback.append("Contact info missing — email, LinkedIn, GitHub add karo.")
    if word_count < 300:
        feedback.append(f"Resume chota hai ({word_count} words) — 300-600 words ideal hai.")
    elif word_count > 800:
        feedback.append(f"Resume bahut lamba hai ({word_count} words) — 600 words tak rakho.")

    # Strengths
    if len(all_skills) >= 8:
        strengths.append(f"Strong skill set — {len(all_skills)} technologies listed hain.")
    if skills_by_cat["frontend"] and skills_by_cat["backend"]:
        strengths.append("Full-stack profile clearly dikhti hai — recruiters ko pasand aata hai.")
    if skills_by_cat["dsa"]:
        strengths.append("DSA skills mentioned hain — product companies ke liye plus point hai.")
    if metrics:
        strengths.append(f"Measurable results hain ({', '.join(metrics[:3])}) — resume strong lagta hai.")
    if len(verbs) >= 5:
        strengths.append(f"{len(verbs)} strong action verbs use kiye hain — professional lagta hai.")
    if sections["achievements"]:
        strengths.append("Achievements section hai — recruiters ka dhyan jata hai isme.")
    if project_count >= 2:
        strengths.append(f"{project_count} projects detect hue — achha portfolio hai.")

    return {
        "total_score":       total,
        "grade":             get_grade(total),
        "breakdown":         scores,
        "skills_by_category": skills_by_cat,
        "all_skills_found":  all_skills,
        "action_verbs":      verbs,
        "weak_words_found":  weak_words,
        "metrics_found":     metrics,
        "sections_present":  sections,
        "spacy_entities":    spacy_data,
        "word_count":        word_count,
        "project_count":     project_count,
        "feedback":          feedback,
        "strengths":         strengths,
        "roast": roast,
    }

def generate_roast(data):
    score = data["total_score"]
    skills = data["all_skills_found"]
    weak_words = data["weak_words_found"]
    metrics = data["metrics_found"]
    word_count = data["word_count"]
    project_count = data["project_count"]
    sections = data["sections_present"]

    roasts = []

    # Score based roast
    if score < 40:
        roasts.append("Bhai ye resume hai ya grocery list? Recruiter ne dekha hoga toh chai pine chale gaye honge! ☕")
    elif score < 55:
        roasts.append("Resume dekh ke lagta hai tune 10 minute mein banaya — aur recruiter ne 5 second mein delete kar diya! 🗑️")
    elif score < 70:
        roasts.append("Bura nahi hai bhai, but recruiter abhi bhi confused hai ki tu developer hai ya 'developed' karna seekh raha hai! 🤔")
    elif score < 85:
        roasts.append("Achha hai bhai! But still — LinkedIn pe 'Open to Work' banner lagana band kar, pehle resume strong kar! 😅")
    else:
        roasts.append("Wah bhai wah! Resume itna strong hai ki recruiter ka phone already ring ho raha hoga! 📱")

    # Skills roast
    if len(skills) < 5:
        roasts.append(f"Sirf {len(skills)} skills? Bhai mera 10 saal ka bhatija bhi zyada skills jaanta hai! 😂")
    if not data["skills_by_category"]["database"]:
        roasts.append("Database skill nahi hai? Bhai data kahan store karega — Excel mein? 😭")
    if not data["skills_by_category"]["dsa"]:
        roasts.append("DSA mention nahi? FAANG companies ne already tera resume blacklist kar diya hoga! 💀")

    # Weak words roast
    if weak_words:
        roasts.append(f"'{ ', '.join(weak_words) }' likha hai resume mein? Bhai ye job application hai, confession nahi! 😬")

    # Metrics roast
    if not metrics:
        roasts.append("Koi numbers nahi hain resume mein — recruiter ko kaise pata chalega ki tune kuch kiya bhi ya bas GitHub pe star diya? ⭐")

    # Word count roast
    if word_count < 200:
        roasts.append(f"Sirf {word_count} words? Bhai meri WhatsApp status teri se zyada detailed hai! 📱")
    elif word_count > 800:
        roasts.append(f"{word_count} words ka resume? Recruiter novel padhne nahi aaya hai interview mein! 📚")

    # Projects roast
    if project_count < 2:
        roasts.append("Ek hi project hai? Bhai ek project se job milti toh sab log Amazon pe bech ke FAANG join kar lete! 😂")

    # Summary roast
    if not sections["summary"]:
        roasts.append("Summary section nahi hai — recruiter ko khud guess karna padega ki tu human hai ya bot! 🤖")

    # Achievements roast
    if not sections["achievements"]:
        roasts.append("Achievements section nahi? Matlab zindagi mein kuch achieve hi nahi kiya? Chal koi nahi, abhi time hai! 💪")

    # Contact roast
    if not sections["contact"]:
        roasts.append("Contact info nahi hai — recruiter carrier pigeon bheje kya tujhe hire karne ke liye? 🐦")

    # Ending motivation
    if score >= 70:
        roasts.append("Overall solid hai bhai — bas thoda aur polish kar, job pakki samajh! 🚀")
    else:
        roasts.append("Chal bhai himmat rakh — sabka pehla resume aisa hi hota hai. Fix kar aur wapas aa! 💪")

    return roasts

def get_grade(score):
    if score >= 85: return "A — Excellent"
    if score >= 70: return "B — Good"
    if score >= 55: return "C — Average"
    return "D — Needs Work"