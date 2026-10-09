
import os
import sys

from flask import Flask, jsonify
from flask_cors import CORS

# Add the ai-ml folder to Python's import path
AI_ML_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "ai-ml")
)
sys.path.insert(0, AI_ML_PATH)

from services.score_service import calculate_success_scores
from ai_ml.recommendations import generate_recommendations

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return jsonify({
        "message": "Student Success Analytics API is running!"
    })


@app.route("/api/dashboard")
def dashboard():
    students = calculate_success_scores()

    return jsonify({
        "total_students": int(len(students)),
        "average_success_score": round(
            float(students["success_score"].mean()), 2
        ),
        "needs_support": int(
            (students["support_status"] == "Needs Support").sum()
        ),
        "needs_attention": int(
            (students["support_status"] == "Needs Attention").sum()
        ),
        "on_track": int(
            (students["support_status"] == "On Track").sum()
        ),
    })


@app.route("/api/students")
def get_students():
    students = calculate_success_scores()

    columns = [
        "student_id",
        "cgpa",
        "attendance",
        "success_score",
        "support_status",
    ]

    return jsonify(
        students[columns].to_dict(orient="records")
    )


@app.route("/api/students/<student_id>/recommendations")
def student_recommendations(student_id):
    students = calculate_success_scores()

    student = students[
        students["student_id"] == student_id
    ]

    if student.empty:
        return jsonify({
            "error": "Student not found"
        }), 404

    student_data = student.iloc[0].to_dict()
    recommendations = generate_recommendations(student_data)

    return jsonify({
        "student_id": student_id,
        "recommendations": recommendations
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)
