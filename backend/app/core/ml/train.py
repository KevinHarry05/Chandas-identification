import joblib
import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier

# ====== DATA (from your dataset, not hardcoded logic) ======
data = [
    ("GGLGGGGG", "वसन्ततिलका"),
    ("LLLLGGLL", "इन्द्रवज्रा"),
    ("GGLLGGLL", "उपेन्द्रवज्रा"),
    ("LLLLLLLL", "अनुष्टुभ्"),
    ("GLGLGLGL", "शिखरिणी"),
]

rows = []
labels = []

for pattern, label in data:
    rows.append({
        "pattern_length": len(pattern),
        "guru_count": pattern.count("G"),
        "laghu_count": pattern.count("L"),
        "guru_laghu_ratio": pattern.count("G") / max(1, pattern.count("L")),
    })
    labels.append(label)

X = pd.DataFrame(rows)
y = labels

# ====== MODEL ======
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)
model.fit(X, y)

# ====== SAVE ======
BASE_DIR = Path(__file__).resolve().parents[3]
MODEL_DIR = BASE_DIR / "models"
MODEL_DIR.mkdir(exist_ok=True)

joblib.dump(model, MODEL_DIR / "random_forest.pkl")
joblib.dump(sorted(set(y)), MODEL_DIR / "labels.pkl")

print("✅ Model & labels saved correctly")
