"""
evaluate_models.py
------------------

Evaluates trained ML models for:
1. Symptom → Remedy prediction
2. Prakriti prediction

This script DOES NOT retrain models.
It only loads saved models and runs test predictions.

Used for:
- Validation
- Debugging
- Project demonstration
"""

import os
import sys
import joblib
import pandas as pd

# -----------------------------
# Path setup
# -----------------------------
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ML_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
sys.path.append(ML_DIR)

from preprocessing.cleaner import clean_text
from preprocessing.feature_encoder import load_tfidf_vectorizer

# -----------------------------
# Paths
# -----------------------------
MODEL_DIR = os.path.join(ML_DIR, "models")

REMEDY_MODEL_PATH = os.path.join(MODEL_DIR, "remedy_model.pkl")
VECTORIZER_PATH = os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl")
PRAKRITI_MODEL_PATH = os.path.join(MODEL_DIR, "prakriti_model.pkl")

PRAKRITI_DATA_PATH = os.path.join(ML_DIR, "data", "Prakriti.csv")


def evaluate_remedy_model():
    print("\n🔹 Evaluating Symptom → Remedy Model")

    if not os.path.exists(REMEDY_MODEL_PATH):
        raise FileNotFoundError("Remedy model not found")

    model = joblib.load(REMEDY_MODEL_PATH)
    vectorizer = load_tfidf_vectorizer()

    test_inputs = [
        "I have fever and sore throat",
        "constipation with indigestion",
        "headache and nausea"
    ]

    print("\nSample Predictions:")
    for text in test_inputs:
        cleaned = clean_text(text)
        vector = vectorizer.transform([cleaned])
        prediction = model.predict(vector)[0]

        print(f"Input: {text}")
        print(f"Predicted Remedy: {prediction}\n")


def evaluate_prakriti_model():
    print("\n🔹 Evaluating Prakriti Model")

    if not os.path.exists(PRAKRITI_MODEL_PATH):
        raise FileNotFoundError("Prakriti model not found")

    model = joblib.load(PRAKRITI_MODEL_PATH)

    # Load label encoder
    label_encoder_path = os.path.join(MODEL_DIR, "prakriti_label_encoder.pkl")
    label_encoder = joblib.load(label_encoder_path)

    df = pd.read_csv(PRAKRITI_DATA_PATH)

    # Normalize column names
    df.columns = df.columns.str.lower().str.strip()

    # Rename dosha → prakriti
    if "dosha" in df.columns:
        df = df.rename(columns={"dosha": "prakriti"})
    else:
        raise ValueError(f"'dosha' column not found. Columns: {df.columns.tolist()}")

    X = df.drop(columns=["prakriti"])

    # Take random samples
    sample = X.sample(5, random_state=42)
    predictions = model.predict(sample)

    # Decode predictions
    decoded_preds = label_encoder.inverse_transform(predictions)

    print("\nSample Prakriti Predictions:")
    for i, pred in enumerate(decoded_preds):
        print(f"Sample {i + 1} → Predicted Prakriti: {pred}")



def main():
    print("✅ Starting Model Evaluation")

    evaluate_remedy_model()
    evaluate_prakriti_model()

    print("\n🎯 Model evaluation completed successfully")


if __name__ == "__main__":
    main()
