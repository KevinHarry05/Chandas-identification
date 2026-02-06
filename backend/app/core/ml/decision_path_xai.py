# ============================================================
# Decision Path Explainability for Random Forest
# ============================================================

from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import VotingClassifier, RandomForestClassifier


def _extract_trees_from_model(model):
    """
    Extract tree estimators from potentially wrapped models.
    Handles: CalibratedClassifierCV, VotingClassifier, RandomForestClassifier
    """
    trees = []
    
    # If wrapped in CalibratedClassifierCV, get base estimator
    if isinstance(model, CalibratedClassifierCV):
        # Try multiple attribute names for compatibility  
        base = getattr(model, 'estimator', None) or getattr(model, 'estimator_', None) or getattr(model, 'base_estimator_', None)
        if base is None:
            return []
        if isinstance(base, VotingClassifier):
            # VotingClassifier case
            for est in base.estimators_:
                if hasattr(est, 'estimators_'):
                    trees.extend(est.estimators_)
                else:
                    trees.append(est)
        elif hasattr(base, 'estimators_'):
            trees.extend(base.estimators_)
        return trees
    
    # Direct ensemble
    if isinstance(model, VotingClassifier):
        for est in model.estimators_:
            if hasattr(est, 'estimators_'):
                trees.extend(est.estimators_)
            else:
                trees.append(est)
        return trees
    
    if hasattr(model, 'estimators_'):
        trees.extend(model.estimators_)
        return trees
    
    return []


def extract_decision_paths(model, feature_vector, feature_names):
    """
    Extract decision rules followed by trees in the Random Forest
    for a given input. Handles calibrated and wrapped models.
    """

    paths = []
    
    # Extract trees from potentially wrapped model
    trees = _extract_trees_from_model(model)
    
    if not trees:
        return []  # Return empty if no trees found

    for tree in trees[:10]:  # Limit to first 10 trees for performance
        try:
            node_indicator = tree.decision_path(feature_vector)
            leaf_id = tree.apply(feature_vector)

            feature = tree.tree_.feature
            threshold = tree.tree_.threshold

            rules = []

            for node_id in node_indicator.indices:
                if leaf_id[0] == node_id:
                    continue

                if feature[node_id] != -2:
                    fname = feature_names[feature[node_id]]
                    fvalue = feature_vector.iloc[0, feature[node_id]]
                    thresh = threshold[node_id]

                    if fvalue <= thresh:
                        rules.append(f"{fname} ≤ {round(thresh, 3)}")
                    else:
                        rules.append(f"{fname} > {round(thresh, 3)}")

            paths.append(rules)
        except Exception:
            # Skip this tree if error
            continue

    return paths
