import os
import joblib
import pandas as pd
import numpy as np

MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'readmission_risk_pipeline.pkl')

_pipeline = None


def load_model():
    """Load the trained pipeline. Returns None if model file not found."""
    global _pipeline
    if _pipeline is None:
        if os.path.exists(MODEL_PATH):
            _pipeline = joblib.load(MODEL_PATH)
    return _pipeline


def model_available() -> bool:
    """Check whether a trained model file exists."""
    return os.path.exists(MODEL_PATH)


def predict(input_dict: dict) -> dict:
    """
    Run prediction on a single patient record.

    Parameters
    ----------
    input_dict : dict
        Keys: age_group, gender, region, department, treatment_type,
              visit_type, length_of_stay_days, treatment_cost, recovery_score

    Returns
    -------
    dict with keys: 'label' (str), 'probabilities' (dict or None)
    """
    pipe = load_model()
    if pipe is None:
        return {'label': 'Model not available', 'probabilities': None}

    feature_order = [
        'age_group', 'gender', 'region', 'department', 'treatment_type',
        'visit_type', 'length_of_stay_days', 'treatment_cost', 'recovery_score',
    ]
    X = pd.DataFrame([{k: input_dict[k] for k in feature_order}])

    label = pipe.predict(X)[0]

    probs = None
    if hasattr(pipe, 'predict_proba'):
        prob_values = pipe.predict_proba(X)[0]
        classes = pipe.classes_
        probs = {cls: round(float(p) * 100, 1) for cls, p in zip(classes, prob_values)}

    return {'label': label, 'probabilities': probs}
