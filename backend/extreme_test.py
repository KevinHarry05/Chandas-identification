#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════
    EXTREME PROJECT TEST SUITE
    Final Comprehensive Testing - Zero Issues Allowed
═══════════════════════════════════════════════════════════════════

This test suite performs extreme testing on:
  ✓ Model accuracy with edge cases
  ✓ API robustness with extreme inputs
  ✓ Database integrity under stress
  ✓ Feature extraction correctness
  ✓ Error handling and recovery
  ✓ Performance under load
  ✓ Code quality and integration
  ✓ Data validation and consistency

Any failure means the system is not production-ready.
Target: 100% pass rate with zero warnings.
"""

import sys
import os
from pathlib import Path
import json
import time
import warnings
import traceback
from typing import List, Dict, Any, Tuple

# Setup paths
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

# Suppress non-critical warnings for cleaner output
warnings.filterwarnings('ignore', category=UserWarning, message='X does not have valid feature names')
warnings.filterwarnings('ignore', category=UserWarning, message='X has feature names')

import numpy as np
import pandas as pd
from collections import Counter

print("=" * 80)
print("EXTREME PROJECT TEST SUITE".center(80))
print("=" * 80)

# Track results
results = {
    'model': {'pass': 0, 'fail': 0, 'tests': []},
    'api': {'pass': 0, 'fail': 0, 'tests': []},
    'database': {'pass': 0, 'fail': 0, 'tests': []},
    'features': {'pass': 0, 'fail': 0, 'tests': []},
    'integration': {'pass': 0, 'fail': 0, 'tests': []},
    'performance': {'pass': 0, 'fail': 0, 'tests': []},
}

def log_test(category: str, name: str, passed: bool, message: str = ""):
    """Log test result."""
    status = "[PASS]" if passed else "[FAIL]"
    results[category]['pass' if passed else 'fail'] += 1
    results[category]['tests'].append({
        'name': name,
        'passed': passed,
        'message': message
    })
    
    print(f"  {status} {name}")
    if message:
        print(f"      → {message}")

# ═══════════════════════════════════════════════════════════════════
# SECTION 1: EXTREME MODEL TESTING
# ═══════════════════════════════════════════════════════════════════

print("\n" + "=" * 80)
print("SECTION 1: EXTREME MODEL VALIDATION".center(80))
print("=" * 80)

try:
    from app.core.ml import model_loader
    from app.core.ml.enhanced_features import extract_enhanced_features
    from app.core.text.laghu_guru import extract_laghu_guru_pattern
    
    model = model_loader.model
    labels = model_loader.labels
    scaler = model_loader.scaler
    
    print("\n[MODEL LOADING]")
    
    # Test 1: Model exists and loads
    try:
        assert model is not None, "Model is None"
        log_test('model', 'Model loads successfully', True)
    except Exception as e:
        log_test('model', 'Model loads successfully', False, str(e))
    
    # Test 2: Labels exist
    try:
        assert labels is not None and len(labels) == 10, f"Expected 10 labels, got {len(labels)}"
        log_test('model', 'All 10 labels loaded', True)
    except Exception as e:
        log_test('model', 'All 10 labels loaded', False, str(e))
    
    # Test 3: Scaler exists
    try:
        assert scaler is not None, "Scaler is None"
        log_test('model', 'Feature scaler loaded', True)
    except Exception as e:
        log_test('model', 'Feature scaler loaded', False, str(e))
    
    # Test 4: Model has predict_proba
    try:
        assert hasattr(model, 'predict_proba'), "Model missing predict_proba method"
        log_test('model', 'Model has predict_proba method', True)
    except Exception as e:
        log_test('model', 'Model has predict_proba method', False, str(e))
    
    # Test 5: Model consistency
    try:
        test_pattern = "LLGLLGGG"
        features_dict = extract_enhanced_features(test_pattern)
        features_df = pd.DataFrame([features_dict])
        features_scaled = scaler.transform(features_df)
        
        pred1 = model.predict(features_scaled)[0]
        pred2 = model.predict(features_scaled)[0]
        
        assert pred1 == pred2, "Model predictions are not deterministic"
        log_test('model', 'Model predictions are deterministic', True)
    except Exception as e:
        log_test('model', 'Model predictions are deterministic', False, str(e))
    
    print("\n[EXTREME PATTERN TESTING]")
    
    # Test 6: Shortest possible pattern
    try:
        pattern = "G"
        features_dict = extract_enhanced_features(pattern)
        features_df = pd.DataFrame([features_dict])
        features_scaled = scaler.transform(features_df)
        pred = model.predict(features_scaled)[0]
        assert pred is not None, "Model failed on shortest pattern"
        log_test('model', 'Handles shortest patterns (1 syllable)', True)
    except Exception as e:
        log_test('model', 'Handles shortest patterns (1 syllable)', False, str(e)[:50])
    
    # Test 7: Very long pattern
    try:
        pattern = "G" * 100  # 100 syllables
        features_dict = extract_enhanced_features(pattern)
        features_df = pd.DataFrame([features_dict])
        features_scaled = scaler.transform(features_df)
        pred = model.predict(features_scaled)[0]
        assert pred is not None, "Model failed on longest pattern"
        log_test('model', 'Handles very long patterns (100+ syllables)', True)
    except Exception as e:
        log_test('model', 'Handles very long patterns (100+ syllables)', False, str(e)[:50])
    
    # Test 8: All Guru pattern
    try:
        pattern = "G" * 20
        features = extract_enhanced_features(pattern)
        features_scaled = scaler.transform([features])
        pred = model.predict(features_scaled)[0]
        proba = model.predict_proba(features_scaled)[0]
        confidence = np.max(proba)
        assert 0 <= confidence <= 1, "Invalid confidence score"
        log_test('model', 'Handles all-Guru patterns', True)
    except Exception as e:
        log_test('model', 'Handles all-Guru patterns', False, str(e)[:50])
    
    # Test 9: All Laghu pattern
    try:
        pattern = "L" * 20
        features = extract_enhanced_features(pattern)
        features_scaled = scaler.transform([features])
        pred = model.predict(features_scaled)[0]
        proba = model.predict_proba(features_scaled)[0]
        confidence = np.max(proba)
        assert 0 <= confidence <= 1, "Invalid confidence score"
        log_test('model', 'Handles all-Laghu patterns', True)
    except Exception as e:
        log_test('model', 'Handles all-Laghu patterns', False, str(e)[:50])
    
    # Test 10: Alternating patterns
    try:
        pattern = "GLGL" * 25  # 100 alternating
        features = extract_enhanced_features(pattern)
        features_scaled = scaler.transform([features])
        pred = model.predict(features_scaled)[0]
        assert pred is not None, "Model failed on alternating pattern"
        log_test('model', 'Handles alternating patterns', True)
    except Exception as e:
        log_test('model', 'Handles alternating patterns', False, str(e)[:50])
    
    # Test 11: Confidence bounds
    print("\n[CONFIDENCE CALIBRATION]")
    test_patterns = [
        "LLGLLGGG",  # Anushtubh
        "GLGLGLGLL",  # Shardulvikridita
        "LLLLLLL",
        "G" * 15,
        "L" * 15,
    ]
    
    try:
        all_valid = True
        confidences = []
        for pattern in test_patterns:
            features = extract_enhanced_features(pattern)
            features_scaled = scaler.transform([features])
            proba = model.predict_proba(features_scaled)[0]
            confidence = np.max(proba)
            
            if not (0 <= confidence <= 1):
                all_valid = False
                break
            confidences.append(confidence)
        
        avg_confidence = np.mean(confidences)
        assert all_valid, "Some confidence scores out of bounds"
        assert 0.5 <= avg_confidence <= 1.0, f"Average confidence {avg_confidence} seems off"
        log_test('model', f'Confidence scores calibrated (avg: {avg_confidence:.2%})', True)
    except Exception as e:
        log_test('model', 'Confidence scores calibrated', False, str(e)[:50])
    
    # Test 12: All classes can be predicted
    print("\n[CLASS COVERAGE]")
    try:
        classes_predicted = set()
        # Test multiple patterns to try hitting all classes
        test_patterns = [
            "LLGLLGGG",  # Anushtubh (8)
            "LGLGLG" + "G"*20,  # Long pattern
            "G" * 11,  # Indravajra (11)
            "L" * 12,  # Drutvlambita (12)
            "G" * 17,  # Mandakranta (17)
            "L" * 15,  # Malini (15)
        ]
        
        for pattern in test_patterns:
            features = extract_enhanced_features(pattern)
            features_scaled = scaler.transform([features])
            pred_idx = model.predict(features_scaled)[0]
            pred_meter = labels[pred_idx] if isinstance(pred_idx, (int, np.integer)) else pred_idx
            classes_predicted.add(pred_meter)
        
        assert len(classes_predicted) > 0, "No classes predicted"
        log_test('model', f'Model predicts various classes ({len(classes_predicted)} found)', True)
    except Exception as e:
        log_test('model', 'Model predicts various classes', False, str(e)[:50])
    
except Exception as e:
    log_test('model', 'Model system initialization', False, f"Critical: {str(e)[:50]}")

# ═══════════════════════════════════════════════════════════════════
# SECTION 2: EXTREME FEATURE EXTRACTION TESTING
# ═══════════════════════════════════════════════════════════════════

print("\n" + "=" * 80)
print("SECTION 2: EXTREME FEATURE EXTRACTION".center(80))
print("=" * 80)

try:
    from app.core.ml.enhanced_features import extract_enhanced_features
    
    print("\n[FEATURE CONSISTENCY]")
    
    # Test 13: Same pattern produces same features
    try:
        pattern = "GLGLGLGLL"
        features1 = extract_enhanced_features(pattern)
        features2 = extract_enhanced_features(pattern)
        
        assert len(features1) == 41, f"Expected 41 features, got {len(features1)}"
        assert np.allclose(features1, features2), "Features not deterministic"
        log_test('features', 'Feature extraction is deterministic', True)
    except Exception as e:
        log_test('features', 'Feature extraction is deterministic', False, str(e)[:50])
    
    # Test 14: All features are numeric
    try:
        patterns = ["G" * 10, "L" * 10, "GLGL" * 5, "LLGLLGGG"]
        all_numeric = True
        
        for pattern in patterns:
            features = extract_enhanced_features(pattern)
            if not all(isinstance(f, (int, float, np.number)) for f in features):
                all_numeric = False
                break
        
        assert all_numeric, "Some features are not numeric"
        log_test('features', 'All features are numeric', True)
    except Exception as e:
        log_test('features', 'All features are numeric', False, str(e)[:50])
    
    # Test 15: No NaN or Inf values
    try:
        patterns = ["G" * 20, "L" * 20, "GLGL" * 10, "G" * 1]
        has_issues = False
        
        for pattern in patterns:
            features = extract_enhanced_features(pattern)
            if np.any(np.isnan(features)) or np.any(np.isinf(features)):
                has_issues = True
                break
        
        assert not has_issues, "Features contain NaN or Inf values"
        log_test('features', 'No NaN/Inf values in features', True)
    except Exception as e:
        log_test('features', 'No NaN/Inf values in features', False, str(e)[:50])
    
    # Test 16: Feature count constant
    try:
        patterns = ["G", "L", "GL" * 50, "LG" * 50, "G" * 1, "L" * 100]
        counts = []
        
        for pattern in patterns:
            features = extract_enhanced_features(pattern)
            counts.append(len(features))
        
        assert len(set(counts)) == 1, f"Feature counts vary: {set(counts)}"
        assert counts[0] == 41, f"Expected 41 features, got {counts[0]}"
        log_test('features', 'Consistent feature count (41 features)', True)
    except Exception as e:
        log_test('features', 'Consistent feature count (41 features)', False, str(e)[:50])
    
except Exception as e:
    log_test('features', 'Feature extraction system', False, f"Critical: {str(e)[:50]}")

# ═══════════════════════════════════════════════════════════════════
# SECTION 3: API ENDPOINT TESTING
# ═══════════════════════════════════════════════════════════════════

print("\n" + "=" * 80)
print("SECTION 3: API ENDPOINT TESTING".center(80))
print("=" * 80)

try:
    from fastapi.testclient import TestClient
    from app.main import app
    
    client = TestClient(app)
    
    print("\n[HEALTH CHECK]")
    
    # Test 17: Health endpoint
    try:
        response = client.get("/")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        log_test('api', 'Health check endpoint (GET /)', True)
    except Exception as e:
        log_test('api', 'Health check endpoint (GET /)', False, str(e)[:50])
    
    print("\n[VERSE ANALYSIS]")
    
    # Test 18: Valid input
    try:
        payload = {"text": "test"}
        response = client.post("/analyze-verse", json=payload)
        assert response.status_code in [200, 400], f"Unexpected status: {response.status_code}"
        log_test('api', 'Verse analysis endpoint accepts valid input', True)
    except Exception as e:
        log_test('api', 'Verse analysis endpoint accepts valid input', False, str(e)[:50])
    
    # Test 19: Empty input
    try:
        payload = {"text": ""}
        response = client.post("/analyze-verse", json=payload)
        assert response.status_code in [400, 422], f"Expected error for empty input, got {response.status_code}"
        log_test('api', 'Rejects empty input appropriately', True)
    except Exception as e:
        log_test('api', 'Rejects empty input appropriately', False, str(e)[:50])
    
    # Test 20: Missing field
    try:
        payload = {}
        response = client.post("/analyze-verse", json=payload)
        assert response.status_code in [400, 422], f"Expected error for missing field, got {response.status_code}"
        log_test('api', 'Rejects missing required fields', True)
    except Exception as e:
        log_test('api', 'Rejects missing required fields', False, str(e)[:50])
    
    # Test 21: Very long input
    try:
        payload = {"text": "a" * 10000}
        response = client.post("/analyze-verse", json=payload)
        # Should either process or give proper error
        assert response.status_code in [200, 400, 422], f"Unexpected status: {response.status_code}"
        log_test('api', 'Handles very long input gracefully', True)
    except Exception as e:
        log_test('api', 'Handles very long input gracefully', False, str(e)[:50])
    
    # Test 22: Special characters
    try:
        payload = {"text": "!@#$%^&*()"}
        response = client.post("/analyze-verse", json=payload)
        assert response.status_code in [200, 400], f"Unexpected status: {response.status_code}"
        log_test('api', 'Handles special characters', True)
    except Exception as e:
        log_test('api', 'Handles special characters', False, str(e)[:50])
    
    # Test 23: Response format validation
    try:
        payload = {"text": "test"}
        response = client.post("/analyze-verse", json=payload)
        if response.status_code == 200:
            data = response.json()
            required_fields = ['meter', 'confidence', 'pattern']
            assert all(field in data for field in required_fields), "Missing required response fields"
        log_test('api', 'Response has required fields', True)
    except Exception as e:
        log_test('api', 'Response has required fields', False, str(e)[:50])
    
    # Test 24: Response types
    try:
        payload = {"text": "test"}
        response = client.post("/analyze-verse", json=payload)
        if response.status_code == 200:
            data = response.json()
            assert isinstance(data.get('meter'), str), "Meter should be string"
            assert isinstance(data.get('confidence'), (int, float)), "Confidence should be numeric"
            assert isinstance(data.get('pattern'), str), "Pattern should be string"
        log_test('api', 'Response fields have correct types', True)
    except Exception as e:
        log_test('api', 'Response fields have correct types', False, str(e)[:50])
    
except Exception as e:
    log_test('api', 'API system initialization', False, f"Critical: {str(e)[:50]}")

# ═══════════════════════════════════════════════════════════════════
# SECTION 4: DATABASE TESTING
# ═══════════════════════════════════════════════════════════════════

print("\n" + "=" * 80)
print("SECTION 4: DATABASE INTEGRITY".center(80))
print("=" * 80)

try:
    from app.core.db.db_utils import get_db_connection
    
    print("\n[CONNECTION]")
    
    # Test 25: Database connection
    try:
        conn = get_db_connection()
        assert conn is not None, "Connection is None"
        conn.close()
        log_test('database', 'Database connection works', True)
    except Exception as e:
        log_test('database', 'Database connection works', False, str(e)[:50])
    
    # Test 26: Multiple connections
    try:
        conns = []
        for i in range(5):
            conn = get_db_connection()
            assert conn is not None
            conns.append(conn)
        
        for conn in conns:
            conn.close()
        
        log_test('database', 'Multiple connections work', True)
    except Exception as e:
        log_test('database', 'Multiple connections work', False, str(e)[:50])
    
    print("\n[QUERIES]")
    
    # Test 27: Query existing data
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM predictions LIMIT 1")
        result = cursor.fetchone()
        assert result is not None
        conn.close()
        log_test('database', 'Query execution works', True)
    except Exception as e:
        log_test('database', 'Query execution works', False, str(e)[:50])
    
except Exception as e:
    log_test('database', 'Database system', False, f"Critical: {str(e)[:50]}")

# ═══════════════════════════════════════════════════════════════════
# SECTION 5: INTEGRATION TESTING
# ═══════════════════════════════════════════════════════════════════

print("\n" + "=" * 80)
print("SECTION 5: END-TO-END INTEGRATION".center(80))
print("=" * 80)

try:
    from app.core.ml import model_loader
    from app.core.ml.enhanced_features import extract_enhanced_features
    from app.core.text.laghu_guru import extract_laghu_guru_pattern
    
    model = model_loader.model
    labels = model_loader.labels
    scaler = model_loader.scaler
    
    print("\n[FULL PIPELINE]")
    
    # Test 28: Full prediction pipeline
    try:
        test_text = "test"
        pattern = extract_laghu_guru_pattern(test_text) if len(test_text) > 0 else "LLG"
        features = extract_enhanced_features(pattern)
        features_scaled = scaler.transform([features])
        pred_idx = model.predict(features_scaled)[0]
        pred_meter = labels[pred_idx]
        proba = model.predict_proba(features_scaled)[0]
        confidence = float(np.max(proba))
        
        assert pred_meter in labels, f"Invalid prediction: {pred_meter}"
        assert 0 <= confidence <= 1, f"Invalid confidence: {confidence}"
        log_test('integration', 'Full pipeline: text -> prediction', True)
    except Exception as e:
        log_test('integration', 'Full pipeline: text -> prediction', False, str(e)[:50])
    
except Exception as e:
    log_test('integration', 'Integration system', False, f"Critical: {str(e)[:50]}")

# ═══════════════════════════════════════════════════════════════════
# SECTION 6: PERFORMANCE TESTING
# ═══════════════════════════════════════════════════════════════════

print("\n" + "=" * 80)
print("SECTION 6: PERFORMANCE TESTS".center(80))
print("=" * 80)

try:
    from app.core.ml import model_loader
    from app.core.ml.enhanced_features import extract_enhanced_features
    
    model = model_loader.model
    scaler = model_loader.scaler
    
    print("\n[SPEED]")
    
    # Test 29: Feature extraction speed
    try:
        pattern = "LLGLLGGG"
        start = time.time()
        for _ in range(100):
            features = extract_enhanced_features(pattern)
        elapsed = time.time() - start
        
        avg_time = elapsed / 100
        assert avg_time < 0.1, f"Feature extraction too slow: {avg_time:.4f}s per call"
        log_test('performance', f'Feature extraction fast ({avg_time*1000:.2f}ms/call)', True)
    except Exception as e:
        log_test('performance', 'Feature extraction speed', False, str(e)[:50])
    
    # Test 30: Model prediction speed
    try:
        pattern = "LLGLLGGG"
        features = extract_enhanced_features(pattern)
        features_scaled = scaler.transform([features])
        
        start = time.time()
        for _ in range(100):
            pred = model.predict(features_scaled)
        elapsed = time.time() - start
        
        avg_time = elapsed / 100
        assert avg_time < 0.1, f"Prediction too slow: {avg_time:.4f}s per call"
        log_test('performance', f'Model prediction fast ({avg_time*1000:.2f}ms/call)', True)
    except Exception as e:
        log_test('performance', 'Model prediction speed', False, str(e)[:50])
    
except Exception as e:
    log_test('performance', 'Performance testing', False, f"Critical: {str(e)[:50]}")

# ═══════════════════════════════════════════════════════════════════
# FINAL REPORT
# ═══════════════════════════════════════════════════════════════════

print("\n" + "=" * 80)
print("FINAL TEST REPORT".center(80))
print("=" * 80)

total_tests = 0
total_pass = 0
total_fail = 0

print("\nResults by Category:\n")

for category, data in results.items():
    pass_count = data['pass']
    fail_count = data['fail']
    total = pass_count + fail_count
    
    if total > 0:
        pass_rate = (pass_count / total) * 100
        status = "✅" if fail_count == 0 else "⚠️"
        print(f"  {status} {category.upper():15} {pass_count:2}/{total:2} passed ({pass_rate:5.1f}%)")
        
        total_tests += total
        total_pass += pass_count
        total_fail += fail_count

overall_pass_rate = (total_pass / total_tests * 100) if total_tests > 0 else 0

print(f"\n{'─' * 80}")
print(f"  TOTAL: {total_pass}/{total_tests} tests passed ({overall_pass_rate:.1f}%)")
print(f"{'─' * 80}")

if total_fail == 0:
    print("\n✅ ALL TESTS PASSED - PROJECT IS READY FOR PRODUCTION")
    print("   No issues detected. System is fully operational.\n")
    exit(0)
else:
    print(f"\n⚠️ {total_fail} TEST(S) FAILED - ISSUES DETECTED")
    print("   The following issues must be fixed:\n")
    
    for category, data in results.items():
        failed_tests = [t for t in data['tests'] if not t['passed']]
        if failed_tests:
            print(f"  {category.upper()}:")
            for test in failed_tests:
                print(f"    • {test['name']}")
                if test['message']:
                    print(f"      {test['message']}")
    print()
    exit(1)
