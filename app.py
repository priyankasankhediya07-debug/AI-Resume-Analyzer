from flask import Flask, request, jsonify
from reportlab.pdfgen import canvas
from flask import send_file
from flask_cors import CORS
import fitz

app = Flask(__name__)
CORS(app)
last_result= {}

@app.route("/")
def home():
    return "AI Resume Analyzer Backend Running Successfully!"

@app.route("/analyze", methods=["POST"])
def analyze_resume():

    file = request.files.get("resume")

    if not file:
        return jsonify({"error": "No resume uploaded"})

    doc = fitz.open(stream=file.read(), filetype="pdf")

    text = ""

    for page in doc:
        text += page.get_text()

    text = text.lower()

    # ---------------- SKILLS ----------------

    skills_db = [
    "python","java","c","c++","html","css","javascript",
    "react","node","express","flask","django","fastapi",
    "sql","mysql","postgresql","mongodb",

    "machine learning","deep learning","artificial intelligence",
    "data science","pandas","numpy","tensorflow","pytorch",

    "aws","azure","google cloud","docker","kubernetes",
    "devops","linux","git","github",

    "cyber security","ethical hacking","network security",
    "penetration testing",

    "android","flutter","react native",

    "ui/ux","figma","canva",

    "power bi","tableau","excel","business analytics",

    "marketing","seo","sales","branding",

    "finance","accounting","investment","banking",

    "recruitment","hr","talent acquisition",

    "iot","arduino","raspberry pi",

    "blockchain","web3",

    "communication","leadership","teamwork",
    "problem solving","project management"
]

    detected_skills = []

    for skill in skills_db:
        if skill in text:
            detected_skills.append(skill.title())

    # ---------------- DOMAIN ----------------
     
    domain = "General"
    domain_scores = {
    "Software Development": 0,
    "Data Science & AI": 0,
    "Cyber Security": 0,
    "Cloud Computing": 0,
    "DevOps": 0,
    "Mobile App Development": 0,
    "UI/UX Design": 0,
    "Business Analytics": 0,
    "Marketing": 0,
    "Finance": 0,
    "Human Resources": 0
    }

    if any(x in text for x in ["python","java","html","css","javascript","react","node","django","flask","fastapi"]):
        domain_scores["Software Development"] += 1
    elif any(x in text for x in ["machine learning","deep learning","artificial intelligence","data science","pandas","numpy","tensorflow","pytorch"]):
        domain = "Data Science & AI"

    elif any(x in text for x in ["cyber security","ethical hacking","penetration testing","network security"]):
        domain = "Cyber Security"

    elif any(x in text for x in ["aws","azure","google cloud","cloud computing"]):
        domain = "Cloud Computing"

    elif any(x in text for x in ["docker","kubernetes","devops","linux"]):
        domain = "DevOps"

    elif any(x in text for x in ["android","flutter","react native"]):
        domain = "Mobile App Development"

    elif any(x in text for x in ["ui/ux","figma","adobe xd","canva"]):
        domain = "UI/UX Design"

    elif any(x in text for x in ["power bi","tableau","business analytics"]):
        domain = "Business Analytics"

    elif any(x in text for x in ["marketing","seo","sales","branding"]):
        domain = "Marketing"

    elif any(x in text for x in ["finance","accounting","investment","banking"]):
        domain = "Finance"

    elif any(x in text for x in ["recruitment","hr","talent acquisition"]):
        domain = "Human Resources"

    elif any(x in text for x in ["healthcare","hospital","medical","nursing"]):
        domain = "Healthcare"

    elif any(x in text for x in ["iot","arduino","raspberry pi"]):
        domain = "Internet of Things"

    elif any(x in text for x in ["blockchain","web3"]):
        domain = "Blockchain"

    elif any(x in text for x in ["project management","scrum","agile"]):
        domain = "Project Management"

    elif any(x in text for x in ["teacher","education","training"]):
        domain = "Education"

    # ---------------- ATS SCORE ----------------

    ats_score = 0

    # Skills
    ats_score += min(len(detected_skills) * 4, 40)

    # Projects
    if "project" in text:
        ats_score += 15

    # Certifications
    if "certificate" in text or "certification" in text:
        ats_score += 15

    # Education
    if "b.tech" in text or "bachelor" in text:
        ats_score += 10

    # Internship / Experience
    if "internship" in text or "experience" in text:
        ats_score += 10

    # Leadership
    if "leadership" in text or "team leader" in text:
        ats_score += 10

    ats_score = min(ats_score, 100)

    # ---------------- STRENGTH ----------------

    if ats_score >= 85:
        strength = "Excellent"
    elif ats_score >= 70:
        strength = "Good"
    elif ats_score >= 50:
        strength = "Average"
    else:
        strength = "Needs Improvement"

    # ---------------- MISSING SKILLS ----------------

    missing_skills = []

    if domain == "Software Development":
        required = ["Python", "HTML", "CSS", "JavaScript", "SQL"]

    elif domain == "Data Science":
        required = ["Python", "Pandas", "Numpy", "SQL", "Power BI"]

    elif domain == "Marketing":
        required = ["SEO", "Communication", "Sales", "Branding"]

    elif domain == "Finance":
        required = ["Excel", "Accounting", "Finance", "Power BI"]

    elif domain == "Human Resources":
        required = ["Communication", "Recruitment", "Leadership"]

    elif domain == "Healthcare":
        required = ["Medical", "Healthcare", "Patient Care"]

    else:
        required = []

    for skill in required:
        if skill.lower() not in text:
            missing_skills.append(skill)

    # ---------------- RECOMMENDATIONS ----------------

    recommendations = [
        "Add more projects",
        "Add measurable achievements",
        "Improve technical keywords"
    ]
    global last_result

    last_result = {
    "ats_score": ats_score,
    "domain": domain,
    "strength": strength,
    "skills": detected_skills,
    "missing_skills": missing_skills,
    "recommendations": recommendations
}
    return jsonify({
        "filename": file.filename,
        "domain": domain,
        "skills": detected_skills,
        "missing_skills": missing_skills,
        "ats_score": ats_score,
        "strength": strength,
        "recommendations": recommendations
    })

@app.route("/download-report")
def download_report():

    pdf_file = "resume_report.pdf"

    c = canvas.Canvas(pdf_file)

    c.setFont("Helvetica-Bold", 20)
    c.drawString(100, 800, "AI Resume Analysis Report")

    c.setFont("Helvetica", 12)
    c.drawString(100, 760, "Generated by AI Resume Analyzer")
    c.drawString(100, 720, f"ATS Score: {last_result['ats_score']}")
    c.drawString(100, 700, f"Domain: {last_result['domain']}")
    c.drawString(100, 680, f"Resume Strength: {last_result['strength']}")
    c.drawString(100, 650, "Detected Skills:")
    c.drawString(120, 630, ",".join(last_result["skills"]))

    c.drawString(100, 600, "Missing Skills:")
    c.drawString(120, 580, ",".join(last_result["missing_skills"]))

    c.drawString(100, 550, "Recommendations:")
    y = 530
    for rec in last_result["recommendations"]:
     c.drawString(120, y, rec)
    y -= 20
    c.drawString(120, 490, "Improve technical keywords")
    c.save()

    return send_file(pdf_file, as_attachment=True)
if __name__ == "__main__":
    app.run(debug=True)