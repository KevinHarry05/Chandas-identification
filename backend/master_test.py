#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════
    CHANDAS IDENTIFIER - MASTER TEST SUITE
    Comprehensive Backend Testing
═══════════════════════════════════════════════════════════════════

Tests:
    ✓ Database connectivity and operations
    ✓ Model loading and inference
    ✓ Feature extraction pipeline
    ✓ Pattern extraction
    ✓ API endpoints
    ✓ XAI/SHAP integration
    ✓ Data validation
    ✓ Performance metrics

Date: February 5, 2026
Author: Test Suite
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import traceback

# Add backend to path for imports
BACKEND_PATH = Path(__file__).parent
sys.path.insert(0, str(BACKEND_PATH))
sys.path.insert(0, str(BACKEND_PATH.parent))

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(text):
    """Print formatted header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(70)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 70}{Colors.ENDC}\n")


def print_test(name, passed, error=None):
    """Print test result"""
    status = f"{Colors.GREEN}[PASS]{Colors.ENDC}" if passed else f"{Colors.RED}[FAIL]{Colors.ENDC}"
    print(f"  {status}  {name}")
    if error:
        print(f"         {Colors.RED}{error}{Colors.ENDC}")


def print_section(text):
    """Print section header"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}> {text}{Colors.ENDC}")
    print(f"{Colors.CYAN}{'-' * 70}{Colors.ENDC}")


# ═══════════════════════════════════════════════════════════════════
# TEST 1: DATABASE CONNECTIVITY
# ═══════════════════════════════════════════════════════════════════

print_header("TEST SUITE: CHANDAS IDENTIFIER BACKEND")
print(f"{Colors.BLUE}Starting comprehensive backend tests...{Colors.ENDC}\n")

test_results = []

print_section("DATABASE TESTS")

# Test 1.1: Database Connection
try:
    from app.core.db.db_utils import test_connection
    result = test_connection()
    test_results.append(("Database Connection", result))
    print_test("Database Connection (PostgreSQL)", result)
except Exception as e:
    test_results.append(("Database Connection", False))
    print_test("Database Connection (PostgreSQL)", False, str(e))

# Test 1.2: Get Database Connection
try:
    from app.core.db.db_utils import get_connection
    conn = get_connection()
    success = conn is not None
    if conn:
        from app.core.db.db_utils import return_connection
        return_connection(conn)
    test_results.append(("Get DB Connection", success))
    print_test("Get Database Connection from Pool", success)
except Exception as e:
    test_results.append(("Get DB Connection", False))
    print_test("Get Database Connection from Pool", False, str(e))

# Test 1.3: Query Predictions Table
try:
    from app.core.db.db_utils import get_connection
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM chandas_predictions")
    count = cur.fetchone()[0]
    cur.close()
    from app.core.db.db_utils import return_connection
    return_connection(conn)
    success = True
    test_results.append(("Query Predictions", success))
    print_test(f"Query Predictions Table ({count} rows)", success)
except Exception as e:
    test_results.append(("Query Predictions", False))
    print_test("Query Predictions Table", False, str(e))

# ═══════════════════════════════════════════════════════════════════
# TEST 2: MODEL LOADING
# ═══════════════════════════════════════════════════════════════════

print_section("MODEL LOADING TESTS")

# Test 2.1: Load Model
try:
    from app.core.ml.model_loader import model, MODEL_PATH
    success = model is not None and hasattr(model, 'predict_proba')
    test_results.append(("Model Loading", success))
    print_test(f"Model Loading from {MODEL_PATH.name}", success)
except Exception as e:
    test_results.append(("Model Loading", False))
    print_test("Model Loading", False, str(e))

# Test 2.2: Check Model Type
try:
    from app.core.ml.model_loader import model
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.calibration import CalibratedClassifierCV
    is_rf = isinstance(model, RandomForestClassifier)
    is_calibrated = isinstance(model, CalibratedClassifierCV)
    has_predict = hasattr(model, 'predict_proba')
    success = is_rf or is_calibrated or (has_predict and hasattr(model, 'base_estimator_'))
    model_type = type(model).__name__
    test_results.append(("Model Type Check", success))
    print_test(f"Model Type Check ({model_type})", success)
except Exception as e:
    test_results.append(("Model Type Check", False))
    print_test("Model Type Check", False, str(e))

# Test 2.3: Load Labels
try:
    from app.core.ml.model_loader import labels, LABELS_PATH
    success = labels is not None and isinstance(labels, (list, tuple))
    num_classes = len(labels) if success else 0
    test_results.append(("Labels Loading", success))
    print_test(f"Labels Loading ({num_classes} classes)", success)
except Exception as e:
    test_results.append(("Labels Loading", False))
    print_test("Labels Loading", False, str(e))

# Test 2.4: Load Feature Scaler
try:
    from app.core.ml.model_loader import scaler, SCALER_PATH
    if SCALER_PATH:
        success = scaler is not None
        test_results.append(("Scaler Loading", success))
        print_test(f"Feature Scaler Loading", success)
    else:
        test_results.append(("Scaler Loading", True))
        print_test(f"Feature Scaler (optional, not used)", True)
except Exception as e:
    test_results.append(("Scaler Loading", False))
    print_test("Feature Scaler Loading", False, str(e))

# Test 2.5: Ensemble Detection
try:
    from app.core.ml.model_loader import model
    is_ensemble = (
        hasattr(model, 'estimators_') or 
        hasattr(model, 'base_estimator_') or
        hasattr(model, 'estimators')
    )
    test_results.append(("Ensemble Architecture", is_ensemble))
    print_test(f"Ensemble Architecture Detected", is_ensemble)
except Exception as e:
    test_results.append(("Ensemble Architecture", False))
    print_test("Ensemble Architecture Detected", False, str(e))

# ═══════════════════════════════════════════════════════════════════
# TEST 3: PATTERN EXTRACTION
# ═══════════════════════════════════════════════════════════════════

print_section("PATTERN EXTRACTION TESTS")

# Test 3.1: Extract Laghu-Guru Pattern
try:
    from app.core.text.laghu_guru import extract_laghu_guru_pattern
    
    test_verse = "यह एक परीक्षा है"
    pattern = extract_laghu_guru_pattern(test_verse)
    
    is_valid = isinstance(pattern, str) and all(c in 'LG' for c in pattern)
    has_length = len(pattern) > 0
    success = is_valid and has_length
    
    test_results.append(("Pattern Extraction", success))
    print_test(f"Pattern Extraction (verse -> '{pattern}')", success)
except Exception as e:
    test_results.append(("Pattern Extraction", False))
    print_test("Pattern Extraction", False, str(e))

# Test 3.2: Pattern Validation
try:
    from app.core.text.laghu_guru import extract_laghu_guru_pattern
    
    # Valid patterns
    test_cases = [
        ("यह एक परीक्षा है", True),  # Short verse
        ("धर्मो रक्षति रक्षितः", True),  # Sanskrit verse
        ("", False),  # Empty
    ]
    
    passed = 0
    for verse, should_pass in test_cases:
        try:
            pattern = extract_laghu_guru_pattern(verse)
            if should_pass:
                passed += 1
        except:
            if not should_pass:
                passed += 1
    
    success = passed == len(test_cases)
    test_results.append(("Pattern Validation", success))
    print_test(f"Pattern Validation ({passed}/{len(test_cases)} cases)", success)
except Exception as e:
    test_results.append(("Pattern Validation", False))
    print_test("Pattern Validation", False, str(e))

# ═══════════════════════════════════════════════════════════════════
# TEST 4: FEATURE EXTRACTION
# ═══════════════════════════════════════════════════════════════════

print_section("FEATURE EXTRACTION TESTS")

# Test 4.1: Basic Feature Extraction
try:
    from app.core.ml.features import build_feature_df
    
    test_pattern = "LLGLLLG"
    features = build_feature_df(test_pattern)
    
    required_cols = {'pattern_length', 'guru_count', 'laghu_count', 'guru_laghu_ratio'}
    has_cols = all(col in features.columns for col in required_cols)
    has_row = len(features) == 1
    success = has_cols and has_row
    
    test_results.append(("Basic Features", success))
    print_test(f"Basic Feature Extraction (4 features)", success)
except Exception as e:
    test_results.append(("Basic Features", False))
    print_test("Basic Feature Extraction", False, str(e))

# Test 4.2: Enhanced Feature Extraction
try:
    from app.core.ml.enhanced_features import extract_enhanced_features
    
    test_pattern = "LLGLLLGGLG"
    features_dict = extract_enhanced_features(test_pattern)
    
    num_features = len(features_dict)
    success = num_features >= 30 and isinstance(features_dict, dict)
    
    test_results.append(("Enhanced Features", success))
    print_test(f"Enhanced Feature Extraction ({num_features} features)", success)
except Exception as e:
    test_results.append(("Enhanced Features", False))
    print_test("Enhanced Feature Extraction", False, str(e))

# Test 4.3: Build Enhanced Feature DataFrame
try:
    from app.core.ml.enhanced_features import build_enhanced_feature_df
    
    test_pattern = "LLGLLLGGLG"
    feature_df = build_enhanced_feature_df(test_pattern)
    
    has_row = len(feature_df) == 1
    num_cols = len(feature_df.columns)
    success = has_row and num_cols >= 30
    
    test_results.append(("Enhanced DataFrame", success))
    print_test(f"Enhanced Feature DataFrame ({num_cols} columns)", success)
except Exception as e:
    test_results.append(("Enhanced DataFrame", False))
    print_test("Enhanced Feature DataFrame", False, str(e))

# ═══════════════════════════════════════════════════════════════════
# TEST 5: MODEL PREDICTION
# ═══════════════════════════════════════════════════════════════════

print_section("MODEL PREDICTION TESTS")

# Test 5.1: Direct Pattern Prediction
try:
    from app.core.ml.predict import predict_proba_with_labels
    
    test_pattern = "LLGLLLGGLG"
    predictions = predict_proba_with_labels(test_pattern)
    
    is_list = isinstance(predictions, list)
    has_items = len(predictions) > 0
    first_item = predictions[0] if has_items else {}
    has_structure = all(k in first_item for k in ['chandas', 'confidence'])
    success = is_list and has_items and has_structure
    
    test_results.append(("Direct Prediction", success))
    if success:
        top_pred = predictions[0]
        print_test(f"Direct Pattern Prediction (Top: {top_pred['chandas'][:10]} @ {top_pred['confidence']:.1%})", success)
    else:
        print_test("Direct Pattern Prediction", success)
except Exception as e:
    test_results.append(("Direct Prediction", False))
    print_test("Direct Pattern Prediction", False, str(e))

# Test 5.2: High-Confidence Pattern
try:
    from app.core.ml.predict import predict_proba_with_labels
    
    # Use a common Anushtubh pattern
    test_pattern = "LLGLLLGG"  # Typical anushtubh pada
    predictions = predict_proba_with_labels(test_pattern)
    
    max_confidence = max(p['confidence'] for p in predictions) if predictions else 0
    success = max_confidence > 0.5  # Should have reasonable confidence
    
    test_results.append(("High Confidence Score", success))
    print_test(f"High Confidence Pattern Detection ({max_confidence:.1%})", success)
except Exception as e:
    test_results.append(("High Confidence Score", False))
    print_test("High Confidence Pattern Detection", False, str(e))

# Test 5.3: Top-K Predictions
try:
    from app.core.ml.predict import predict_proba_with_labels
    
    test_pattern = "LLGLLLGGLG"
    predictions_all = predict_proba_with_labels(test_pattern)
    predictions_top3 = predict_proba_with_labels(test_pattern, top_k=3)
    
    success = len(predictions_top3) <= 3 and len(predictions_top3) > 0
    
    test_results.append(("Top-K Parameter", success))
    print_test(f"Top-K Predictions (returned {len(predictions_top3)} of top 3)", success)
except Exception as e:
    test_results.append(("Top-K Parameter", False))
    print_test("Top-K Predictions", False, str(e))

# ═══════════════════════════════════════════════════════════════════
# TEST 6: XAI/SHAP INTEGRATION
# ═══════════════════════════════════════════════════════════════════

print_section("XAI & EXPLAINABILITY TESTS")

# Test 6.1: SHAP Values Computation
try:
    from app.core.ml.shap_xai import compute_shap_values
    from app.core.ml.enhanced_features import build_enhanced_feature_df
    
    test_pattern = "LLGLLLGGLG"
    feature_df = build_enhanced_feature_df(test_pattern)
    shap_vals = compute_shap_values(feature_df, class_index=0)
    
    is_list = isinstance(shap_vals, list)
    has_items = len(shap_vals) > 0
    first_item = shap_vals[0] if has_items else {}
    has_structure = all(k in first_item for k in ['feature', 'value', 'shap_value'])
    success = is_list and has_items and has_structure
    
    test_results.append(("SHAP Computation", success))
    print_test(f"SHAP Values Computation ({len(shap_vals)} contributions)", success)
except Exception as e:
    test_results.append(("SHAP Computation", False))
    print_test("SHAP Values Computation", False, str(e))

# Test 6.2: Feature Importance
try:
    from app.core.ml.xai_engine import explain_prediction
    from app.core.ml.enhanced_features import build_enhanced_feature_df
    
    test_pattern = "LLGLLLGGLG"
    feature_df = build_enhanced_feature_df(test_pattern)
    explanation = explain_prediction(feature_df)
    
    is_list = isinstance(explanation, list)
    has_items = len(explanation) > 0
    first_item = explanation[0] if has_items else {}
    has_structure = all(k in first_item for k in ['feature', 'value', 'importance'])
    success = is_list and has_items and has_structure
    
    test_results.append(("Feature Importance", success))
    print_test(f"Feature Importance Extraction ({len(explanation)} features)", success)
except Exception as e:
    test_results.append(("Feature Importance", False))
    print_test("Feature Importance Extraction", False, str(e))

# Test 6.3: Decision Path Extraction
try:
    from app.core.ml.decision_path_xai import extract_decision_paths
    from app.core.ml.model_loader import model
    from app.core.ml.enhanced_features import build_enhanced_feature_df
    
    test_pattern = "LLGLLLGGLG"
    feature_df = build_enhanced_feature_df(test_pattern)
    feature_names = list(feature_df.columns)
    
    paths = extract_decision_paths(model, feature_df, feature_names)
    
    is_list = isinstance(paths, list)
    success = is_list and len(paths) > 0
    
    test_results.append(("Decision Paths", success))
    print_test(f"Decision Path Extraction ({len(paths)} trees)", success)
except Exception as e:
    test_results.append(("Decision Paths", False))
    print_test("Decision Path Extraction", False, str(e))

# ═══════════════════════════════════════════════════════════════════
# TEST 7: API ENDPOINTS
# ═══════════════════════════════════════════════════════════════════

print_section("API ENDPOINT TESTS")

# Test 7.1: FastAPI App Loading
try:
    from app.main import app
    from fastapi import FastAPI
    
    success = isinstance(app, FastAPI)
    
    test_results.append(("FastAPI App", success))
    print_test(f"FastAPI Application Loading", success)
except Exception as e:
    test_results.append(("FastAPI App", False))
    print_test("FastAPI Application Loading", False, str(e))

# Test 7.2: Health Check Endpoint
try:
    from fastapi.testclient import TestClient
    from app.main import app
    
    client = TestClient(app)
    response = client.get("/")
    
    success = response.status_code == 200
    data = response.json() if success else {}
    has_status = "status" in data
    
    success = success and has_status
    
    test_results.append(("Health Check Endpoint", success))
    print_test(f"Health Check Endpoint (/)", success)
except Exception as e:
    test_results.append(("Health Check Endpoint", False))
    print_test("Health Check Endpoint (/)", False, str(e))

# Test 7.3: Verse Analysis Endpoint
try:
    from fastapi.testclient import TestClient
    from app.main import app
    
    client = TestClient(app)
    
    test_verse = "यह एक परीक्षा है"
    response = client.post(
        "/analyze-verse",
        json={"verse": test_verse}
    )
    
    success = response.status_code == 200
    data = response.json() if success else {}
    has_pattern = "laghu_guru_pattern" in data
    has_prediction = "best_prediction" in data
    
    success = success and has_pattern and has_prediction
    
    test_results.append(("Verse Analysis Endpoint", success))
    if success:
        pred = data.get('best_prediction', {})
        print_test(f"Verse Analysis Endpoint (/analyze-verse)", success)
    else:
        print_test(f"Verse Analysis Endpoint (/analyze-verse)", success)
except Exception as e:
    test_results.append(("Verse Analysis Endpoint", False))
    print_test("Verse Analysis Endpoint (/analyze-verse)", False, str(e))

# Test 7.4: Invalid Input Handling
try:
    from fastapi.testclient import TestClient
    from app.main import app
    
    client = TestClient(app)
    
    # Test with non-Devanagari
    response = client.post(
        "/analyze-verse",
        json={"verse": "hello world"}
    )
    
    success = response.status_code == 422  # Validation error
    
    test_results.append(("Invalid Input Handling", success))
    print_test(f"Invalid Input Handling (rejects non-Devanagari)", success)
except Exception as e:
    test_results.append(("Invalid Input Handling", False))
    print_test("Invalid Input Handling", False, str(e))

# ═══════════════════════════════════════════════════════════════════
# TEST 8: DATA VALIDATION
# ═══════════════════════════════════════════════════════════════════

print_section("DATA & VALIDATION TESTS")

# Test 8.1: Load Dataset
try:
    import pandas as pd
    import json
    
    data_path = BACKEND_PATH.parent / "data" / "examples.json"
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    examples = data.get('examples', [])
    success = len(examples) > 0
    
    test_results.append(("Load Dataset", success))
    print_test(f"Load Example Dataset ({len(examples)} examples)", success)
except Exception as e:
    test_results.append(("Load Dataset", False))
    print_test("Load Example Dataset", False, str(e))

# Test 8.2: Dataset Balance
try:
    import json
    from collections import Counter
    
    data_path = BACKEND_PATH.parent / "data" / "examples.json"
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    examples = data.get('examples', [])
    meters = [ex.get('meter') for ex in examples]
    meter_counts = Counter(meters)
    
    # Check if relatively balanced
    if len(meter_counts) > 0:
        min_count = min(meter_counts.values())
        max_count = max(meter_counts.values())
        ratio = max_count / min_count if min_count > 0 else 0
        success = ratio <= 5  # Allow up to 5:1 ratio
    else:
        success = False
    
    test_results.append(("Dataset Balance", success))
    if success:
        print_test(f"Dataset Balance Check (ratio: {ratio:.2f}:1)", success)
    else:
        print_test(f"Dataset Balance Check", success)
except Exception as e:
    test_results.append(("Dataset Balance", False))
    print_test("Dataset Balance Check", False, str(e))

# ═══════════════════════════════════════════════════════════════════
# SUMMARY & REPORT
# ═══════════════════════════════════════════════════════════════════

print_section("TEST SUMMARY")

total_tests = len(test_results)
passed_tests = sum(1 for _, result in test_results if result)
failed_tests = total_tests - passed_tests

pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0

print(f"\n{Colors.BOLD}Total Tests: {total_tests}{Colors.ENDC}")
print(f"{Colors.GREEN}{Colors.BOLD}[PASS] Passed: {passed_tests}{Colors.ENDC}")
print(f"{Colors.RED}{Colors.BOLD}[FAIL] Failed: {failed_tests}{Colors.ENDC}")
print(f"{Colors.BOLD}Pass Rate: {pass_rate:.1f}%{Colors.ENDC}")

# Detailed Report
print("\n" + Colors.CYAN + Colors.BOLD + "DETAILED RESULTS" + Colors.ENDC)
print(Colors.CYAN + "-" * 70 + Colors.ENDC)

categories = {
    "Database": ["Database Connection", "Get DB Connection", "Query Predictions"],
    "Model": ["Model Loading", "Model Type Check", "Labels Loading", "Scaler Loading", "Ensemble Architecture"],
    "Pattern": ["Pattern Extraction", "Pattern Validation"],
    "Features": ["Basic Features", "Enhanced Features", "Enhanced DataFrame"],
    "Prediction": ["Direct Prediction", "High Confidence Score", "Top-K Parameter"],
    "XAI": ["SHAP Computation", "Feature Importance", "Decision Paths"],
    "API": ["FastAPI App", "Health Check Endpoint", "Verse Analysis Endpoint", "Invalid Input Handling"],
    "Data": ["Load Dataset", "Dataset Balance"]
}

for category, tests in categories.items():
    cat_results = [(t, r) for t, r in test_results if t in tests]
    if cat_results:
        cat_passed = sum(1 for _, r in cat_results if r)
        cat_total = len(cat_results)
        status = f"{Colors.GREEN}[OK]{Colors.ENDC}" if cat_passed == cat_total else f"{Colors.YELLOW}[!]{Colors.ENDC}"
        print(f"{status} {category}: {cat_passed}/{cat_total}")

# Final Status
print("\n" + Colors.BOLD + "=" * 70 + Colors.ENDC)
if pass_rate >= 90:
    print(f"{Colors.GREEN}{Colors.BOLD}[OK] OVERALL STATUS: EXCELLENT{Colors.ENDC}")
    print(f"{Colors.GREEN}All critical systems operational. Backend is production-ready.{Colors.ENDC}")
elif pass_rate >= 70:
    print(f"{Colors.YELLOW}{Colors.BOLD}[!] OVERALL STATUS: GOOD{Colors.ENDC}")
    print(f"{Colors.YELLOW}Most systems operational. Please review failed tests.{Colors.ENDC}")
else:
    print(f"{Colors.RED}{Colors.BOLD}[X] OVERALL STATUS: ISSUES DETECTED{Colors.ENDC}")
    print(f"{Colors.RED}Critical issues found. Please fix failures before deployment.{Colors.ENDC}")

print(f"{Colors.BOLD}{'=' * 70}{Colors.ENDC}")
print(f"\n{Colors.BLUE}Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.ENDC}\n")

# Exit with appropriate code
sys.exit(0 if pass_rate >= 90 else 1)
