
from pathlib import Path

import numpy as np
import pandas as pd


# Find the project's database/data folder automatically
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "database" / "data"


def generate_synthetic_data(number_of_students=240):
    """Generate fictional student records across seven data sources."""

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Fixed seed makes the sample data reproducible
    rng = np.random.default_rng(42)

    student_ids = [
        f"STU{i:04d}"
        for i in range(1, number_of_students + 1)
    ]

    # 1. Academic data
    academic = pd.DataFrame({
        "student_id": student_ids,
        "cgpa": np.round(
            np.clip(rng.normal(7.2, 1.2, number_of_students), 3, 10), 2
        ),
        "internal_marks": np.round(
            np.clip(rng.normal(70, 15, number_of_students), 0, 100), 1
        ),
        "backlogs": rng.integers(0, 4, number_of_students)
    })

    # 2. Attendance data
    attendance = pd.DataFrame({
        "student_id": student_ids,
        "attendance": np.round(
            np.clip(rng.normal(78, 13, number_of_students), 30, 100), 1
        )
    })

    # 3. Learning Management System (LMS) data
    lms = pd.DataFrame({
        "student_id": student_ids,
        "lms_logins_weekly": rng.poisson(4, number_of_students),
        "assignment_completion": np.round(
            rng.uniform(20, 100, number_of_students), 1
        )
    })

    # 4. Engagement data
    engagement = pd.DataFrame({
        "student_id": student_ids,
        "events_attended": rng.integers(0, 9, number_of_students),
        "certifications": rng.integers(0, 6, number_of_students),
        "hackathons": rng.integers(0, 4, number_of_students)
    })

    # 5. Placement preparation data
    placement = pd.DataFrame({
        "student_id": student_ids,
        "aptitude_score": np.round(
            rng.uniform(20, 100, number_of_students), 1
        ),
        "coding_score": np.round(
            rng.uniform(10, 100, number_of_students), 1
        ),
        "mock_interview": np.round(
            rng.uniform(20, 100, number_of_students), 1
        )
    })

    # 6. Skills assessment data
    skills = pd.DataFrame({
        "student_id": student_ids,
        "technical_skills": np.round(
            rng.uniform(20, 100, number_of_students), 1
        ),
        "communication": np.round(
            rng.uniform(20, 100, number_of_students), 1
        )
    })

    # 7. Student and faculty feedback
    feedback = pd.DataFrame({
        "student_id": student_ids,
        "satisfaction": rng.integers(1, 6, number_of_students),
        "faculty_feedback": rng.integers(1, 6, number_of_students)
    })

    # Save each source separately
    datasets = {
        "academic.csv": academic,
        "attendance.csv": attendance,
        "lms.csv": lms,
        "engagement.csv": engagement,
        "placement.csv": placement,
        "skills.csv": skills,
        "feedback.csv": feedback
    }

    for filename, dataframe in datasets.items():
        dataframe.to_csv(DATA_DIR / filename, index=False)
        print(f"Created: {filename} ({len(dataframe)} students)")

    print("\nSynthetic data generation completed!")
    print(f"Files saved in: {DATA_DIR}")


if __name__ == "__main__":
    generate_synthetic_data()
