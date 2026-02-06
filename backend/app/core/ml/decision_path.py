import pandas as pd

# ✅ Correct import path
from .model_loader import model


def extract_decision_paths(feature_df: pd.DataFrame, max_trees: int = 3):
    """
    Extract real decision paths from RandomForest trees.

    Parameters
    ----------
    feature_df : pd.DataFrame
        Single-row feature dataframe
    max_trees : int
        Number of trees to analyze

    Returns
    -------
    list[list[dict]]
        Decision paths per tree
    """

    if feature_df.shape[0] != 1:
        raise ValueError("Decision path expects exactly one input sample")

    X = feature_df.values
    feature_names = feature_df.columns

    decision_paths = []

    for tree in model.estimators_[:max_trees]:
        tree_ = tree.tree_

        node_indicator = tree.decision_path(X)
        leaf_id = tree.apply(X)

        sample_id = 0
        node_index = node_indicator.indices[
            node_indicator.indptr[sample_id]:
            node_indicator.indptr[sample_id + 1]
        ]

        path = []

        for node_id in node_index:
            if node_id == leaf_id[sample_id]:
                continue

            feature_index = tree_.feature[node_id]
            threshold = tree_.threshold[node_id]

            if feature_index < 0:
                continue

            feature_name = feature_names[feature_index]
            actual_value = float(X[sample_id, feature_index])

            decision = "<=" if actual_value <= threshold else ">"

            path.append({
                "feature": feature_name,
                "threshold": float(threshold),
                "actual_value": actual_value,
                "decision": decision
            })

        decision_paths.append(path)

    return decision_paths
