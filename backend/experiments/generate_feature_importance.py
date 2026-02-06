import joblib
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# -----------------------------
# CONFIG
# -----------------------------
MODEL_PATH = Path("backend/models/random_forest.pkl")
OUTPUT_PATH = Path("feature_importance.pdf")

FEATURE_NAMES = [
    "pattern_length",
    "guru_count",
    "laghu_count",
    "guru_laghu_ratio"
]

# -----------------------------
# LOAD MODEL
# -----------------------------
if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Model not found at {MODEL_PATH}")

model = joblib.load(MODEL_PATH)

if not hasattr(model, "feature_importances_"):
    raise ValueError("Loaded model does not expose feature_importances_")

importances = model.feature_importances_

if len(importances) != len(FEATURE_NAMES):
    raise ValueError("Feature count mismatch between model and feature list")

# -----------------------------
# SORT FEATURES
# -----------------------------
indices = np.argsort(importances)[::-1]
sorted_features = [FEATURE_NAMES[i] for i in indices]
sorted_importances = importances[indices]

# -----------------------------
# PLOT
# -----------------------------
plt.figure(figsize=(6, 4))
plt.bar(sorted_features, sorted_importances)
plt.ylabel("Importance Score")
plt.xlabel("Prosodic Features")
plt.title("Feature Importance for Sanskrit Chandas Classification")
plt.tight_layout()

# -----------------------------
# SAVE
# -----------------------------
plt.savefig(OUTPUT_PATH)
plt.close()

print(f"Feature importance graph saved to: {OUTPUT_PATH}")
