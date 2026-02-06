# backend/app/core/ml/model_loader.py

from pathlib import Path
import joblib

# ------------------------------------------------------------------
# Paths
# ------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[3]  # backend/
MODEL_DIR = BASE_DIR / "models"

# Try enhanced model first, fall back to basic model
ENHANCED_MODEL_PATH = MODEL_DIR / "random_forest_enhanced.pkl"
ENHANCED_LABELS_PATH = MODEL_DIR / "labels_enhanced.pkl"
ENHANCED_SCALER_PATH = MODEL_DIR / "scaler_enhanced.pkl"
BASIC_MODEL_PATH = MODEL_DIR / "random_forest.pkl"
BASIC_LABELS_PATH = MODEL_DIR / "labels.pkl"

if ENHANCED_MODEL_PATH.exists() and ENHANCED_LABELS_PATH.exists():
    MODEL_PATH = ENHANCED_MODEL_PATH
    LABELS_PATH = ENHANCED_LABELS_PATH
    SCALER_PATH = ENHANCED_SCALER_PATH
    print("[OK] Loading enhanced model with advanced features")
else:
    MODEL_PATH = BASIC_MODEL_PATH
    LABELS_PATH = BASIC_LABELS_PATH
    SCALER_PATH = None
    print("[!] Loading basic model with 4 features")

# ------------------------------------------------------------------
# Load model, labels, and scaler
# ------------------------------------------------------------------
if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")

if not LABELS_PATH.exists():
    raise FileNotFoundError(f"Labels file not found: {LABELS_PATH}")

model = joblib.load(MODEL_PATH)
labels = joblib.load(LABELS_PATH)

# Load scaler if available
scaler = None
if SCALER_PATH and SCALER_PATH.exists():
    scaler = joblib.load(SCALER_PATH)
    print("[OK] Feature scaler loaded")

# ------------------------------------------------------------------
# Sanity checks (NO hardcoding)
# ------------------------------------------------------------------
if not hasattr(model, "predict_proba"):
    raise TypeError("Loaded model does not support predict_proba()")

if not isinstance(labels, (list, tuple)):
    raise TypeError("Labels must be a list or tuple")

if len(labels) != len(model.classes_):
    raise ValueError(
        "Mismatch between number of labels and model classes"
    )
