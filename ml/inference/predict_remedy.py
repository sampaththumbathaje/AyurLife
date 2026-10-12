"""
predict_remedy.py
-----------------

Inference module for Ayurvedic remedy prediction.

Loads:
- Trained Linear SVM model
- Trained TF-IDF vectorizer

Performs:
- Text cleaning
- Feature transformation
- Remedy prediction

Used by:
- Flask backend (ml_service)
"""

import os
import sys
import joblib
from typing import Optional

# -----------------------------
# Path setup
# -----------------------------
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ML_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
sys.path.append(ML_DIR)

from preprocessing.cleaner import clean_text
from preprocessing.feature_encoder import load_tfidf_vectorizer

# -----------------------------
# Model paths
# -----------------------------
MODEL_DIR = os.path.join(ML_DIR, "models")
REMEDY_MODEL_PATH = os.path.join(MODEL_DIR, "remedy_model.pkl")


class RemedyPredictor:
    """
    Wrapper class for Remedy Prediction.
    Loads model and vectorizer once.
    """

    def __init__(self):
        if not os.path.exists(REMEDY_MODEL_PATH):
            raise FileNotFoundError("Remedy model not found. Train the model first.")

        self.model = joblib.load(REMEDY_MODEL_PATH)
        self.vectorizer = load_tfidf_vectorizer()

    def predict(self, text: Optional[str]) -> Optional[str]:
        """
        Predicts Ayurvedic remedy from symptom text.

        Parameters
        ----------
        text : str
            User-entered symptom text

        Returns
        -------
        str or None
            Predicted remedy name
        """

        if not text or not isinstance(text, str):
            return None

        cleaned_text = clean_text(text)
        vector = self.vectorizer.transform([cleaned_text])

        prediction = self.model.predict(vector)
        return prediction[0]


# -----------------------------
# Standalone testing
# -----------------------------
if __name__ == "__main__":
    predictor = RemedyPredictor()

    test_input = "I have fever and sore throat"
    result = predictor.predict(test_input)

    print(f"Input: {test_input}")
    print(f"Predicted Remedy: {result}")
