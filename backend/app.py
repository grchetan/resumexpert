from flask import Flask, request, jsonify
from flask_cors import CORS
from analyzer import calculate_score

app = Flask(__name__)
CORS(app)

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    resume_text = data.get("text", "")

    if not resume_text.strip():
        return jsonify({"error": "Resume text khali hai!"}), 400

    result = calculate_score(resume_text)
    return jsonify(result)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "running"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
    