
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "database" / "data"


def load_student_data():
    files = [
        "academic.csv",
        "attendance.csv",
        "lms.csv",
        "engagement.csv",
        "placement.csv",
        "skills.csv",
        "feedback.csv",
    ]

    dataframes = [pd.read_csv(DATA_DIR / name) for name in files]
    students = dataframes[0]

    for dataframe in dataframes[1:]:
        students = students.merge(dataframe, on="student_id", how="inner")

    return students


def calculate_success_scores():
    df = load_student_data()

    # Academic performance
    df["academic_score"] = (
        0.6 * df["cgpa"] * 10
        + 0.3 * df["internal_marks"]
        + 0.1 * ((3 - df["backlogs"]).clip(0, 3) / 3 * 100)
    ).clip(0, 100)

    # Attendance and learning activity
    df["attendance_score"] = df["attendance"].clip(0, 100)

    df["lms_score"] = (
        0.7 * df["assignment_completion"]
        + 0.3 * (df["lms_logins_weekly"] / 7 * 100).clip(0, 100)
    ).clip(0, 100)

    # Engagement
    df["engagement_score"] = (
        0.4 * (df["events_attended"] / 8 * 100).clip(0, 100)
        + 0.35 * (df["certifications"] / 5 * 100).clip(0, 100)
        + 0.25 * (df["hackathons"] / 3 * 100).clip(0, 100)
    ).clip(0, 100)

    # Placement readiness
    df["placement_score"] = (
        0.25 * df["aptitude_score"]
        + 0.25 * df["coding_score"]
        + 0.20 * df["mock_interview"]
        + 0.20 * df["technical_skills"]
        + 0.10 * df["communication"]
    ).clip(0, 100)

    # Overall score out of 100
    df["success_score"] = (
        0.30 * df["academic_score"]
        + 0.20 * df["attendance_score"]
        + 0.15 * df["lms_score"]
        + 0.10 * df["engagement_score"]
        + 0.25 * df["placement_score"]
    ).round(2)

    df["support_status"] = df["success_score"].apply(
        lambda score: (
            "Needs Support" if score < 50
            else "Needs Attention" if score < 70
            else "On Track"
        )
    )

    return df


if __name__ == "__main__":
    students = calculate_success_scores()

    output_file = DATA_DIR / "student_success_scores.csv"
    students.to_csv(output_file, index=False)

    print("\n=== STUDENT SUCCESS ANALYTICS ===")
    print(f"Total students: {len(students)}")
    print(f"Average success score: {students['success_score'].mean():.2f}/100")

    print("\nSupport categories:")
    print(students["support_status"].value_counts().to_string())

    print("\nFirst 10 students:")
    print(
        students[["student_id", "success_score", "support_status"]]
        .head(10)
        .to_string(index=False)
    )

    print(f"\nResults saved to: {output_file}")
