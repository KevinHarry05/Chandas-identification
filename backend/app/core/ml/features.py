import pandas as pd


def build_feature_df(laghu_guru_pattern: str) -> pd.DataFrame:
    """
    Converts a Laghu–Guru pattern into a numerically stable
    feature DataFrame for ML models.

    Input:
        laghu_guru_pattern: str (e.g. "GLGLGGLG")

    Output:
        pd.DataFrame with fixed numeric features
    """

    if not isinstance(laghu_guru_pattern, str) or len(laghu_guru_pattern) == 0:
        raise ValueError("Invalid Laghu–Guru pattern")

    pattern_length = len(laghu_guru_pattern)
    guru_count = laghu_guru_pattern.count("G")
    laghu_count = laghu_guru_pattern.count("L")

    # Prevent division instability
    guru_laghu_ratio = (
        guru_count / laghu_count if laghu_count > 0 else float(guru_count)
    )

    features = {
        "pattern_length": float(pattern_length),
        "guru_count": float(guru_count),
        "laghu_count": float(laghu_count),
        "guru_laghu_ratio": float(guru_laghu_ratio),
    }

    # IMPORTANT: column order must remain fixed
    return pd.DataFrame([features])
