# ============================================================
# Counterfactual Explanation Engine
# Semantically meaningful modifications based on prosody rules
# ============================================================

import pandas as pd
import numpy as np

def generate_counterfactuals(model, feature_vector, original_prediction, labels=None, max_changes=5):
    """
    Generate semantically meaningful counterfactual explanations.
    
    Instead of arbitrary +1 modifications, we make prosody-aware changes:
    - Modify guru/laghu counts in valid ranges
    - Maintain realistic feature relationships
    - Generate interpretable "what-if" scenarios
    
    Args:
        model: Trained model
        feature_vector: Original feature DataFrame (single row)
        original_prediction: Original predicted class index
        labels: List of class labels (optional)
        max_changes: Maximum number of counterfactuals to return
    
    Returns:
        List of counterfactual scenarios with meaningful changes
    """
    counterfactuals = []
    original_values = feature_vector.iloc[0].to_dict()
    
    # Define semantically meaningful modifications
    modifications = [
        # Guru/Laghu balance changes
        {"feature": "guru_laghu_ratio", "change": 0.1, "description": "Increase guru ratio slightly"},
        {"feature": "guru_laghu_ratio", "change": -0.1, "description": "Decrease guru ratio slightly"},
        
        # Pattern length modifications
        {"feature": "pattern_length", "change": 1, "description": "Add one syllable"},
        {"feature": "pattern_length", "change": -1, "description": "Remove one syllable"},
        
        # N-gram pattern changes
        {"feature": "glg_count", "change": 1, "description": "Add one G-L-G pattern"},
        {"feature": "lgl_count", "change": 1, "description": "Add one L-G-L pattern"},
        {"feature": "gg_count", "change": 1, "description": "Add one G-G bigram"},
        {"feature": "ll_count", "change": 1, "description": "Add one L-L bigram"},
        
        # Runs modifications
        {"feature": "max_guru_run", "change": 1, "description": "Extend longest guru sequence"},
        {"feature": "max_laghu_run", "change": 1, "description": "Extend longest laghu sequence"},
        
        # Percentage adjustments
        {"feature": "guru_percentage", "change": 0.05, "description": "Increase guru percentage"},
        {"feature": "guru_percentage", "change": -0.05, "description": "Decrease guru percentage"},
    ]
    
    for mod in modifications:
        if mod["feature"] not in feature_vector.columns:
            continue
            
        modified = feature_vector.copy()
        original_val = modified.iloc[0][mod["feature"]]
        new_val = original_val + mod["change"]
        
        # Validate modifications stay in reasonable ranges
        if new_val < 0:
            continue
        
        if "ratio" in mod["feature"] and new_val > 5:
            continue
            
        if "percentage" in mod["feature"] and (new_val < 0 or new_val > 1):
            continue
        
        modified.iloc[0, modified.columns.get_loc(mod["feature"])] = new_val
        
        try:
            new_pred = model.predict(modified)[0]
            
            # Only include if prediction changes
            if new_pred != original_prediction:
                cf = {
                    "changed_feature": mod["feature"],
                    "original_value": float(original_val),
                    "new_value": float(new_val),
                    "change_description": mod["description"],
                    "original_prediction": int(original_prediction),
                    "new_prediction": int(new_pred)
                }
                
                if labels:
                    cf["original_chandas"] = labels[original_prediction]
                    cf["new_chandas"] = labels[new_pred]
                
                counterfactuals.append(cf)
                
                if len(counterfactuals) >= max_changes:
                    break
                    
        except Exception:
            continue
    
    return counterfactuals
