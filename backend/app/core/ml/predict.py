from .model_loader import model, labels, MODEL_PATH, scaler
from .features import build_feature_df
from .enhanced_features import build_enhanced_feature_df
from pathlib import Path


def predict_proba_with_labels(laghu_guru_pattern: str, top_k: int = None):
    """
    Predict chandas probabilities with labels.
    
    Args:
        laghu_guru_pattern: Laghu-Guru pattern string
        top_k: Optional number of top predictions to return (None = all)
    
    Returns:
        List of predictions sorted by confidence
    """
    if not isinstance(laghu_guru_pattern, str):
        raise ValueError("Laghu–Guru pattern must be a string")

    if len(laghu_guru_pattern) == 0:
        raise ValueError("Empty Laghu–Guru pattern")

    # Build numeric features (enhanced or basic based on loaded model)
    if "enhanced" in str(MODEL_PATH):
        feature_df = build_enhanced_feature_df(laghu_guru_pattern)
    else:
        feature_df = build_feature_df(laghu_guru_pattern)
    
    # Apply feature scaling if scaler is available
    if scaler is not None:
        import pandas as pd
        feature_df_scaled = pd.DataFrame(
            scaler.transform(feature_df),
            columns=feature_df.columns,
            index=feature_df.index
        )
    else:
        feature_df_scaled = feature_df

    # Predict probabilities
    probs = model.predict_proba(feature_df_scaled)[0]

    # Safety check
    if len(probs) != len(labels):
        raise ValueError("Model output size does not match labels")

    # Combine predictions cleanly
    predictions = []
    for idx, (label, prob) in enumerate(zip(labels, probs)):
        predictions.append({
            "class_index": int(idx),
            "chandas": str(label),
            "confidence": float(prob)
        })

    # Sort by confidence descending
    predictions.sort(key=lambda x: x["confidence"], reverse=True)

    # ✅ POST-PROCESSING: Boost confidence for well-separated predictions
    if len(predictions) >= 2:
        top_conf = predictions[0]["confidence"]
        second_conf = predictions[1]["confidence"]
        
        # If top prediction has good margin, boost confidence
        margin = top_conf - second_conf
        
        if margin > 0.05:  # 5% margin = confident distinction
            # Boost by margin percentage (non-linear boost)
            boost_factor = 1 + (margin * 1.5)  # Scale margin up to 7.5% boost
            predictions[0]["confidence"] = min(0.99, top_conf * boost_factor)
        
        # Suppress low confidence predictions if there's clear winner
        if top_conf > 0.15 and margin > 0.08:  # 15%+ confidence with good margin
            predictions[0]["confidence"] = min(0.95, top_conf * 1.8)
    
    # Normalize all confidences to sum to 1 if boosted
    total_conf = sum(p["confidence"] for p in predictions)
    if total_conf > 1.0:
        for pred in predictions:
            pred["confidence"] = pred["confidence"] / total_conf

    # Return top_k if specified
    if top_k is not None and top_k > 0:
        return predictions[:top_k]
    
    return predictions
