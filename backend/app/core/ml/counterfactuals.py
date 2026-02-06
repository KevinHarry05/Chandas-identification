import copy
from .predict import predict_proba_with_labels

def generate_counterfactuals(feature_df, target_class_index):
    base_pred = predict_proba_with_labels(feature_df)[target_class_index]["confidence"]
    counterfactuals = []

    for col in feature_df.columns:
        perturbed = feature_df.copy()
        perturbed[col] *= 0.9

        new_pred = predict_proba_with_labels(perturbed)[target_class_index]["confidence"]

        if new_pred < base_pred:
            counterfactuals.append({
                "changed_feature": col,
                "original_value": float(feature_df[col].iloc[0]),
                "new_value": float(perturbed[col].iloc[0]),
                "confidence_drop": base_pred - new_pred,
            })

    return counterfactuals
