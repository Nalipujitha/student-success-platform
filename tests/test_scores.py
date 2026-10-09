from backend.services.score_service import calculate_success_scores


def test_student_scores_are_generated():
    students = calculate_success_scores()

    assert len(students) == 240
    assert "student_id" in students.columns
    assert "support_status" in students.columns


def test_support_status_values_are_valid():
    students = calculate_success_scores()

    valid_statuses = {"Needs Support", "Needs Attention", "On Track"}
    assert set(students["support_status"].unique()).issubset(valid_statuses)
