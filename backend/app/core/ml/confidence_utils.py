# ============================================================
# Confidence Utilities
# ============================================================

def confidence_level(score: float) -> str:
    """
    Convert numeric confidence into a human-readable level.

    This is NOT hardcoding predictions.
    It is a post-model interpretability layer.
    """

    if score >= 0.45:
        return "high"
    elif score >= 0.25:
        return "medium"
    else:
        return "low"
