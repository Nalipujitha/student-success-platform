import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "ai-ml"))
sys.path.insert(0, str(PROJECT_ROOT))

from ai_ml.risk_model import train_risk_model, predict_student_risk
from backend.services.score_service import calculate_success_scores


def test_risk_model():
    students = calculate_success_scores()
    result = train_risk_model(students)

    assert len(students) == 240
    assert 0 <= result["accuracy"] <= 1

    student = students.iloc[0].to_dict()
    prediction = predict_student_risk(result["model"], student)

    assert prediction["predicted_status"] in [
        "Needs Support",
        "Needs Attention",
        "On Track",
    ]
    assert 0 <= prediction["confidence"] <= 1
