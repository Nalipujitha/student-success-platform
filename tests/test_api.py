import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "ai-ml"))
sys.path.insert(0, str(PROJECT_ROOT / "backend"))
sys.path.insert(0, str(PROJECT_ROOT))

from backend.app import app


def test_home_endpoint():
    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    assert "message" in response.get_json()


def test_dashboard_endpoint():
    client = app.test_client()
    response = client.get("/api/dashboard")

    assert response.status_code == 200
    data = response.get_json()

    assert data["total_students"] == 240
    assert "average_success_score" in data
    assert "needs_support" in data
    assert "needs_attention" in data
    assert "on_track" in data


def test_students_endpoint():
    client = app.test_client()
    response = client.get("/api/students")

    assert response.status_code == 200
    students = response.get_json()

    assert len(students) == 240
    assert "student_id" in students[0]
    assert "support_status" in students[0]


def test_student_recommendations_endpoint():
    client = app.test_client()
    response = client.get("/api/students/STU0001/recommendations")

    assert response.status_code == 200
    data = response.get_json()

    assert data["student_id"] == "STU0001"
    assert "recommendations" in data


def test_unknown_student_recommendations():
    client = app.test_client()
    response = client.get(
        "/api/students/UNKNOWN999/recommendations"
    )

    assert response.status_code == 404
    assert response.get_json()["error"] == "Student not found"

