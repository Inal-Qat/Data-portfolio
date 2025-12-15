# model loading + prediction tool
import os
from typing import Dict, Any

import pandas as pd
import joblib
from langchain_core.tools import tool

from .data_tools import df  # same df with engineered features

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODELS_DIR = os.path.join(PROJECT_ROOT, "models")


def load_model():
    """Load the trained RandomForest return model pipeline."""
    path = os.path.join(MODELS_DIR, "order_return_model.pkl")
    model = joblib.load(path)
    return model


model = load_model()


@tool
def predict_return(order_features: Dict[str, Any]) -> str:
    """
    Predict the probability that a given order will be returned.
    Input: a JSON-like dict of feature_name -> value.
    """
    X_new = pd.DataFrame([order_features])

    try:
        proba = model.predict_proba(X_new)[0, 1]
        pred = model.predict(X_new)[0]
    except Exception as e:
        return f"Error during prediction: {e}"

    label = "return" if pred == 1 else "not return"

    return (
        f"Predicted probability of return: {proba:.3f} "
        f"(model predicts this order will **{label}**). "
        f"Note: the model is weak (ROC-AUC ≈ 0.50), "
        f"so treat this as a rough risk indicator, not a precise forecast."
    )