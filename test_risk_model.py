import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "ai-ml"))

from ai_ml.risk_model import train_risk_model, predict_student_risk
from backend.services.score_service import calculate_success_scores

students = calculate_success_scores()
result = train_risk_model(students)

print("\n=== STUDENT RISK MODEL TEST ===")
print("Students:", len(students))
print("Test accuracy:", result["accuracy"])

student = students.iloc[0].to_dict()
prediction = predict_student_risk(result["model"], student)

print("Student ID:", student["student_id"])
print("Actual status:", student["support_status"])
print("Predicted status:", prediction["predicted_status"])
print("Confidence:", prediction["confidence"])
