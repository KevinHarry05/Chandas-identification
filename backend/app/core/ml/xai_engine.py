# ============================================================
# True Explainable AI Engine for Chandas Prediction
# ============================================================

import pandas as pd
from pathlib import Path
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import VotingClassifier, RandomForestClassifier

# Import from model_loader instead to avoid duplicate loading
from app.core.ml.model_loader import model


def _extract_base_model(model):
    """
    Extract the actual ML model from potential wrappers.
    Handles: CalibratedClassifierCV, VotingClassifier, RandomForestClassifier
    """
    if isinstance(model, CalibratedClassifierCV):
        # Try multiple attribute names for compatibility
        return getattr(model, 'estimator', None) or getattr(model, 'estimator_', None) or getattr(model, 'base_estimator_', None)
    return model


def _get_feature_importances(model):
    """
    Extract feature importances from ensemble model.
    """
    base_model = _extract_base_model(model)
    
    if base_model is None:
        raise AttributeError("Could not extract base model from wrapper")
    
    if isinstance(base_model, VotingClassifier):
        # Get from first estimator (usually RandomForest)
        first_est = base_model.estimators_[0]
        if hasattr(first_est, 'feature_importances_'):
            return first_est.feature_importances_
    
    if hasattr(base_model, 'feature_importances_'):
        return base_model.feature_importances_
    
    raise AttributeError("Model does not support feature_importances_")


def explain_prediction(feature_vector: pd.DataFrame):
    """
    Generate a true XAI explanation based on
    feature importance from the underlying ensemble model.
    """
    
    # Get feature names from the dataframe
    feature_names = list(feature_vector.columns)
    
    # Extract feature importances
    importances = _get_feature_importances(model)

    explanation = []

    for feature, value, importance in zip(
        feature_names,
        feature_vector.iloc[0],
        importances
    ):
        explanation.append({
            "feature": feature,
            "value": round(float(value), 3),
            "importance": round(float(importance), 3)
        })

    # Sort by importance (descending)
    explanation.sort(
        key=lambda x: x["importance"],
        reverse=True
    )

    return explanation
