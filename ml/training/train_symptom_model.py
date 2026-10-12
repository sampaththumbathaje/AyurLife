"""
train_symptom_model.py
----------------------

Trains a machine learning model to predict Ayurvedic remedies
based on user-entered symptoms.

Algorithm:
- TF-IDF Vectorization
- Linear Support Vector Machine (LinearSVC)

Dataset:
- ayur_real.csv

Outputs:
- ml/models/tfidf_vectorizer.pkl
- ml/models/remedy_model.pkl
"""

import os
import sys
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, classification_report

# -----------------------------
# Path setup
# -----------------------------
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ML_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
sys.path.append(ML_DIR)

from preprocessing.cleaner import clean_text
from preprocessing.feature_encoder import build_tfidf_vectorizer

# -----------------------------
# Paths
# -----------------------------
DATA_PATH = os.path.join(ML_DIR, "data", "ayur_real.csv")
MODEL_DIR = os.path.join(ML_DIR, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "remedy_model.pkl")
VECTORIZER_PATH = os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl")


def main():
    print("🔹 Loading dataset...")
    df = pd.read_csv(DATA_PATH)

    # Normalize column names
    df.columns = df.columns.str.strip().str.lower()

    if "symptoms" not in df.columns or "remedy" not in df.columns:
        raise ValueError(
            "Dataset must contain 'symptoms' and 'remedy' columns"
        )

    # Clean and prepare data
    df["symptoms"] = df["symptoms"].astype(str)
    df["remedy"] = df["remedy"].astype(str)
    df = df.dropna(subset=["symptoms", "remedy"])

    print("🔹 Cleaning symptom text...")
    df["cleaned_symptoms"] = df["symptoms"].apply(clean_text)

    X = df["cleaned_symptoms"].tolist()
    y = df["remedy"].tolist()

    # -----------------------------
    # Train-test split
    # -----------------------------
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    # -----------------------------
    # TF-IDF Vectorization
    # -----------------------------
    print("🔹 Building TF-IDF vectorizer...")
    vectorizer = build_tfidf_vectorizer(X_train)

    # 🔥 SAVE FITTED VECTORIZER
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(vectorizer, VECTORIZER_PATH)
    print(f"💾 Vectorizer saved at: {VECTORIZER_PATH}")

    X_train_vec = vectorizer.transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    # -----------------------------
    # Train Linear SVM
    # -----------------------------
    print("🔹 Training Linear SVM model...")
    model = LinearSVC(
        C=1.0,
        max_iter=5000,
        random_state=42
    )

    model.fit(X_train_vec, y_train)

    # -----------------------------
    # Evaluation
    # -----------------------------
    y_pred = model.predict(X_test_vec)

    accuracy = accuracy_score(y_test, y_pred)
    print("\n✅ Model Training Completed")
    print(f"📊 Accuracy: {accuracy * 100:.2f}%\n")
    print("📄 Classification Report:")
    print(classification_report(y_test, y_pred))

    # -----------------------------
    # Save model
    # -----------------------------
    joblib.dump(model, MODEL_PATH)
    print(f"\n💾 Model saved at: {MODEL_PATH}")


if __name__ == "__main__":
    main()
