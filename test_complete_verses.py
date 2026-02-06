#!/usr/bin/env python
"""Test with COMPLETE verses"""

import sys
from pathlib import Path

backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from app.core.text.laghu_guru import extract_laghu_guru_pattern
from app.core.ml.predict import predict_proba_with_labels

# COMPLETE verses (full metrical lines)
complete_verses = [
    "नमस्ते रुद्रमन्यव उतोत इषवे नमः बाहुभ्यामुत ते नमः",  # Indravajra - complete
    "सर्वे भवन्तु सुखिनः सर्वे सन्तु निरामयाः सर्वे भद्राणि पश्यन्तु मा कश्चिद्दुःखभाग्भवेत्",  # Anushtubh
]

print("=" * 70)
print("🧪 Testing with COMPLETE Verses")
print("=" * 70)

for verse in complete_verses:
    print(f"\n📖 Verse: {verse}")
    pattern = extract_laghu_guru_pattern(verse)
    print(f"🔤 Pattern: {pattern} (length: {len(pattern)})")
    
    predictions = predict_proba_with_labels(pattern)
    best = predictions[0]
    
    print(f"✅ Prediction: {best['chandas']}")
    print(f"📊 Confidence: {best['confidence']:.2%}")

print("\n" + "=" * 70)
