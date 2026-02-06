import shap
import pandas as pd

# ✅ Correct import path (NO guessing, NO relative confusion)
from .model_loader import model, scaler


# Initialize TreeExplainer ONCE (important for performance & stability)
# For ensemble/calibrated models, extract base estimator
try:
    base_model = model
    
    # Handle CalibratedClassifierCV - extract first calibrated classifier's estimator
    if hasattr(model, 'calibrated_classifiers_'):
        # Get the first calibrated classifier's base estimator
        base_model = model.calibrated_classifiers_[0].estimator
        print(f"✅ Extracted base estimator from CalibratedClassifierCV: {type(base_model)}")
    elif hasattr(model, 'base_estimator'):
        base_model = model.base_estimator
        print(f"✅ Extracted base estimator: {type(base_model)}")
    
    # Handle VotingClassifier - use Random Forest component
    if hasattr(base_model, 'named_estimators_'):
        # VotingClassifier - use Random Forest component
        base_model = base_model.named_estimators_['rf']
        print(f"✅ Extracted Random Forest from ensemble: {type(base_model)}")
    
    _explainer = shap.TreeExplainer(base_model)
    print(f"✅ SHAP explainer initialized successfully")
except Exception as e:
    print(f"⚠️  SHAP initialization error: {e}")
    raise


def compute_shap_values(feature_df: pd.DataFrame, class_index: int):
    """
    Compute true SHAP values for a given class prediction.

    Parameters
    ----------
    feature_df : pd.DataFrame
        Single-row feature dataframe used for prediction
    class_index : int
        Index of predicted class

    Returns
    -------
    list[dict]
        SHAP contribution per feature
    """

    if feature_df.shape[0] != 1:
        raise ValueError("SHAP expects exactly one input sample")

    try:
        shap_values = _explainer.shap_values(feature_df)
        
        # Handle different SHAP return formats
        # For binary/multi-class: shap_values is list of arrays (one per class)
        if isinstance(shap_values, list):
            if len(shap_values) == 0:
                return []
            
            # Clamp class_index to valid range
            safe_class_index = min(class_index, len(shap_values) - 1)
            if safe_class_index < 0:
                safe_class_index = 0
            
            class_shap_values = shap_values[safe_class_index][0]
        else:
            # Single array case
            class_shap_values = shap_values[0]
        
        # Convert numpy arrays to Python floats
        import numpy as np
        
        explanations = []
        for feature, value, shap_val in zip(
            feature_df.columns,
            feature_df.iloc[0].values,
            class_shap_values
        ):
            # Handle numpy arrays by extracting scalar value
            if isinstance(shap_val, (np.ndarray, np.generic)):
                shap_val = float(np.asarray(shap_val).flat[0])
            else:
                shap_val = float(shap_val)
                
            if isinstance(value, (np.ndarray, np.generic)):
                value = float(np.asarray(value).flat[0])
            else:
                value = float(value)
            
            explanations.append({
                "feature": str(feature),
                "value": value,
                "shap_value": shap_val
            })

        return explanations
        
    except Exception as e:
        # Log error but don't crash - return empty explanations gracefully
        print(f"⚠️  SHAP computation error: {type(e).__name__}: {e}")
        return []
