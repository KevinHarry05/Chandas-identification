#!/usr/bin/env python
"""Test model confidence directly"""

import sys
from pathlib import Path

backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from app.core.text.laghu_guru import extract_laghu_guru_pattern
from app.core.ml.model_loader import model, labels, scaler
from app.core.ml.predict import predict_proba_with_labels

# Test verses
test_verses = [
    "यो वै स परम ब्रह्म तस्य नाम सत्यम्।",
    "भगवान भवसागरोद्धारक।",
    "मा गमो यातन प्रिये भरत।",
    "रामराज्यं नृपतेः कृतं।",
]

print("=" * 70)
print("🧪 Testing Model Confidence Directly")
print("=" * 70)

for verse in test_verses:
    print(f"\n📖 Verse: {verse}")
    pattern = extract_laghu_guru_pattern(verse)
    print(f"🔤 Pattern: {pattern} (length: {len(pattern)})")
    
    predictions = predict_proba_with_labels(pattern)
    best = predictions[0]
    
    print(f"✅ Prediction: {best['chandas']}")
    print(f"📊 Confidence: {best['confidence']:.2%}")
    print(f"   Alternatives:")
    for p in predictions[1:4]:
        print(f"     - {p['chandas']}: {p['confidence']:.2%}")

print("\n" + "=" * 70)
