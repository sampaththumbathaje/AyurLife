"""
ml_service.py
-------------

Service layer for Machine Learning operations.

Acts as a bridge between Flask backend and ML models.

Models handled:
- Symptom → Remedy prediction
- Prakriti prediction
"""

# ML imports
from ml.inference.predict_remedy import RemedyPredictor
from ml.inference.predict_prakriti import PrakritiPredictor
from ml.inference.questionnaire_logic import build_ml_input


class MLService:
    """
    Central ML service.
    Loads ML models once and reuses them.
    """

    _remedy_predictor = None
    _prakriti_predictor = None

    # -----------------------------
    # Remedy Prediction
    # -----------------------------
    @classmethod
    def predict_remedy(cls, symptoms: str):
        """
        Predict Ayurvedic remedy from symptoms text.
        """
        if cls._remedy_predictor is None:
            cls._remedy_predictor = RemedyPredictor()

        return cls._remedy_predictor.predict(symptoms)

    # -----------------------------
    # Prakriti Prediction
    # -----------------------------
    @classmethod
    def predict_prakriti(cls, answers: dict):
        """
        Predict Prakriti from questionnaire answers.
        """
        ml_input = build_ml_input(answers)

        if not ml_input:
            return None

        if cls._prakriti_predictor is None:
            cls._prakriti_predictor = PrakritiPredictor()

        return cls._prakriti_predictor.predict(ml_input)
