from flask import Flask, request, jsonify
from flask_cors import CORS
from analyzer import calculate_score
from db import save_analysis, get_history
import fitz
import uuid

app = Flask(__name__)
CORS(app)

@app.route("/analyze", methods=["POST"])
def analyze():
    resume_text = ""

    if request.content_type and "multipart" in request.content_type:
        file = request.files.get("file")
        if not file:
            return jsonify({"error": "File nahi mili!"}), 400
        pdf = fitz.open(stream=file.read(), filetype="pdf")
        for page in pdf:
            resume_text += page.get_text()
    else:
        data = request.get_json()
        resume_text = data.get("text", "")

    if not resume_text.strip():
        return jsonify({"error": "Resume text khali hai!"}), 400

    result = calculate_score(resume_text)
    analysis_id = str(uuid.uuid4())[:8]
    result["id"] = analysis_id
    save_analysis(analysis_id, resume_text, result)
    return jsonify(result)

@app.route("/history", methods=["GET"])
def history():
    return jsonify(get_history())

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "running"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)