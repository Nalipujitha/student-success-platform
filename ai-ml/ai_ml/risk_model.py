
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


FEATURES = [
    "cgpa",
    "attendance",
    "internal_marks",
    "backlogs",
]


def train_risk_model(data):
    """Train a demo model using student support labels."""

    dataset = data[FEATURES + ["support_status"]].dropna().copy()

    X = dataset[FEATURES]
    y = dataset["support_status"]

    if len(dataset) < 20 or y.nunique() < 2:
        raise ValueError(
            "Need at least 20 students and 2 support-status classes."
        )

    # Stratify only when every class has at least 2 students
    class_counts = y.value_counts()
    stratify_labels = y if class_counts.min() >= 2 else None

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=stratify_labels,
    )

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        class_weight="balanced",
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    return {
        "model": model,
        "accuracy": round(
            float(accuracy_score(y_test, predictions)), 3
        ),
        "features": FEATURES,
    }


def predict_student_risk(model, student_data):
    """Predict a student's support category."""

    student_df = pd.DataFrame([
        {feature: student_data[feature] for feature in FEATURES}
    ])

    prediction = model.predict(student_df)[0]
    probabilities = model.predict_proba(student_df)[0]

    return {
        "predicted_status": str(prediction),
        "confidence": round(float(max(probabilities)), 3),
    }
