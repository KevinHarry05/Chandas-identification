# backend/app/core/ml/preprocess.py

import pandas as pd

def build_feature_df(lg_pattern: str) -> pd.DataFrame:
    """
    Converts Laghu–Guru pattern into numeric ML features.
    """

    if not lg_pattern or not isinstance(lg_pattern, str):
        raise ValueError("Invalid Laghu–Guru pattern")

    guru_count = lg_pattern.count("G")
    laghu_count = lg_pattern.count("L")
    pattern_length = len(lg_pattern)

    if pattern_length == 0:
        raise ValueError("Empty Laghu–Guru pattern")

    guru_laghu_ratio = guru_count / max(laghu_count, 1)

    return pd.DataFrame([{
        "pattern_length": float(pattern_length),
        "guru_count": float(guru_count),
        "laghu_count": float(laghu_count),
        "guru_laghu_ratio": float(guru_laghu_ratio)
    }])
