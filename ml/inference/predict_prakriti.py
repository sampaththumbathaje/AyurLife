"""
predict_prakriti.py
-------------------

Inference module for Prakriti prediction.
"""

import os
import sys
import joblib
import pandas as pd
from typing import Dict, Optional

# -----------------------------
# Path setup
# -----------------------------
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ML_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
sys.path.append(ML_DIR)

# -----------------------------
# Model paths
# -----------------------------
MODEL_DIR = os.path.join(ML_DIR, "models")
PRAKRITI_MODEL_PATH = os.path.join(MODEL_DIR, "prakriti_model.pkl")
LABEL_ENCODER_PATH = os.path.join(MODEL_DIR, "prakriti_label_encoder.pkl")

# -----------------------------
# Expected feature schema
# (MUST MATCH TRAINING DATA)
# -----------------------------
PRAKRITI_FEATURES = [
    "body size",
    "body weight",
    "height",
    "bone structure",
    "complexion",
    "general feel of skin",
    "texture of skin",
    "hair color",
    "appearance of hair",
    "shape of face",
    "eyes",
    "eyelashes",
    "blinking of eyes",
    "cheeks",
    "nose",
    "teeth and gums",
    "lips",
    "nails",
    "appetite",
    "liking tastes"
]


class PrakritiPredictor:
    """
    Wrapper class for Prakriti prediction.
    """

    def __init__(self):
        if not os.path.exists(PRAKRITI_MODEL_PATH):
            raise FileNotFoundError("❌ Prakriti model not found. Train the model first.")

        self.model = joblib.load(PRAKRITI_MODEL_PATH)
        self.label_encoder = joblib.load(LABEL_ENCODER_PATH)

    def predict(self, questionnaire_answers: Dict[str, str]):

        if not questionnaire_answers or not isinstance(questionnaire_answers, dict):
            raise ValueError("❌ Invalid questionnaire input")

        # Normalize
        questionnaire_answers = {
            k.lower().strip(): str(v).lower().strip()
            for k, v in questionnaire_answers.items()
        }

        # Strict alignment
        aligned_input = {}

        for feature in PRAKRITI_FEATURES:
            if feature not in questionnaire_answers:
                raise ValueError(f"❌ Missing feature for ML model: {feature}")
            aligned_input[feature] = questionnaire_answers[feature]

        print("🧠 FINAL ML INPUT:", aligned_input)

        input_df = pd.DataFrame([aligned_input])

        # Prediction
        encoded_pred = self.model.predict(input_df)[0]
        decoded_pred = self.label_encoder.inverse_transform([encoded_pred])[0]

        # Probabilities
        probabilities = self.model.predict_proba(input_df)[0]
        class_labels = self.label_encoder.classes_

        prob_dict = {
            class_labels[i]: float(probabilities[i])
            for i in range(len(class_labels))
        }

        print("🔍 Probabilities:", prob_dict)

        return {
            "prediction": decoded_pred,
            "probabilities": prob_dict
        }



# -----------------------------
# Standalone testing
# -----------------------------
if __name__ == "__main__":
    predictor = PrakritiPredictor()

    sample_input = {
        "body size": "slim",
        "body weight": "low",
        "height": "tall",
        "bone structure": "light",
        "complexion": "dark",
        "general feel of skin": "dry",
        "texture of skin": "dry",
        "hair color": "black",
        "appearance of hair": "dry",
        "shape of face": "angular",
        "eyes": "small",
        "eyelashes": "scanty",
        "blinking of eyes": "excessive",
        "cheeks": "sunken",
        "nose": "crooked",
        "teeth and gums": "irregular",
        "lips": "dry",
        "nails": "brittle",
        "appetite": "irregular",
        "liking tastes": "pungent"
    }

    result = predictor.predict(sample_input)
    print("✅ Predicted Prakriti:", result)

    
