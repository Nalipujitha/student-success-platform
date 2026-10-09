
import pandas as pd


def generate_recommendations(student):
    """
    Generate explainable recommendations from student performance data.
    The student argument should be a pandas Series or dictionary.
    """

    if isinstance(student, dict):
        get_value = student.get
    else:
        get_value = student.get

    recommendations = []

    # Attendance recommendations
    attendance = float(get_value("attendance", 0) or 0)

    if attendance < 75:
        recommendations.append({
            "area": "Attendance",
            "priority": "High",
            "message": (
                "Create an attendance improvement plan "
                "and follow up weekly."
            )
        })

    # Academic recommendations
    cgpa = float(get_value("cgpa", 0) or 0)

    if cgpa < 6.5:
        recommendations.append({
            "area": "Academics",
            "priority": "High",
            "message": (
                "Provide subject-wise tutoring, revision "
                "sessions, and practice questions."
            )
        })

    # Placement recommendations
    coding_score = float(get_value("coding_score", 0) or 0)
    aptitude_score = float(get_value("aptitude_score", 0) or 0)

    if coding_score < 60:
        recommendations.append({
            "area": "Coding",
            "priority": "Medium",
            "message": (
                "Follow a weekly coding practice plan "
                "with progressively harder problems."
            )
        })

    if aptitude_score < 60:
        recommendations.append({
            "area": "Aptitude",
            "priority": "Medium",
            "message": (
                "Practice quantitative aptitude and "
                "logical reasoning regularly."
            )
        })

    # LMS engagement recommendations
    assignment_completion = float(
        get_value("assignment_completion", 100) or 0
    )

    if assignment_completion < 70:
        recommendations.append({
            "area": "Learning Engagement",
            "priority": "Medium",
            "message": (
                "Set weekly learning goals and complete "
                "pending online assignments."
            )
        })

    if not recommendations:
        recommendations.append({
            "area": "Overall Progress",
            "priority": "Low",
            "message": (
                "Maintain current learning habits and "
                "continue building academic and career skills."
            )
        })

    return recommendations
