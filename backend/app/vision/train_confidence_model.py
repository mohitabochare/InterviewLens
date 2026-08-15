import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib


CSV_PATH = "app/vision/data/training_data.csv"
MODEL_PATH = "app/vision/data/confidence_model.pkl"


def load_data():
    df = pd.read_csv(CSV_PATH)

    # head_pose is text ("Looking Center", etc) - convert to numeric
    # columns the model can actually use (one-hot encoding)
    df = pd.get_dummies(df, columns=["head_pose"])

    feature_cols = [
        col for col in df.columns
        if col not in ("timestamp", "confidence_score", "label")
    ]

    X = df[feature_cols]
    y = df["label"]

    return X, y, feature_cols


def train():
    X, y, feature_cols = load_data()

    print(f"Loaded {len(X)} labeled rows.")
    print(f"Label counts:\n{y.value_counts()}\n")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    print(f"Test accuracy: {accuracy:.2f}")
    print("\nDetailed report:")
    print(classification_report(y_test, predictions))

    print("Learned feature weights:")
    for name, coef in zip(feature_cols, model.coef_[0]):
        print(f"  {name}: {coef:.3f}")

    joblib.dump({"model": model, "feature_cols": feature_cols}, MODEL_PATH)
    print(f"\nModel saved to {MODEL_PATH}")


if __name__ == "__main__":
    train()