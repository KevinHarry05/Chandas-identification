# ============================================================
# Advanced ML Training with Confidence Calibration & Ensemble
# ============================================================

import joblib
import json
from pathlib import Path
from collections import Counter
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.metrics import classification_report, accuracy_score, log_loss, brier_score_loss
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd

from .load_full_data import load_examples_json
from .enhanced_features import extract_enhanced_features
from ..text.laghu_guru import extract_laghu_guru_pattern


def build_advanced_dataset(
    json_path=None,
    use_provided_patterns=True,
    min_pattern_length: int = 8
):
    """
    Build dataset with advanced enhanced features.
    Uses augmented dataset by default for better training.
    """
    # Try augmented dataset first, fall back to original
    if json_path is None:
        augmented_path = Path("data/examples_augmented.json")
        if augmented_path.exists():
            json_path = str(augmented_path)
            print(f"📈 Using augmented dataset: {json_path}")
        else:
            json_path = None  # Will use default in load_examples_json
    
    examples = load_examples_json(json_path)
    
    print(f"📚 Loaded {len(examples)} examples from JSON")
    
    features_list = []
    labels_list = []
    skipped = 0
    skipped_short = 0
    
    for idx, example in enumerate(examples):
        try:
            meter = example.get('meter')
            if not meter:
                skipped += 1
                continue
            
            # Get pattern
            if use_provided_patterns and 'pattern' in example:
                pattern = example['pattern']
            elif 'text' in example:
                pattern = extract_laghu_guru_pattern(example['text'])
            else:
                skipped += 1
                continue
            
            if len(pattern) < min_pattern_length:
                skipped_short += 1
                continue

            # Extract enhanced features
            features = extract_enhanced_features(pattern)
            features_list.append(features)
            labels_list.append(meter)
            
        except Exception as e:
            print(f"⚠️  Skipped example {idx}: {e}")
            skipped += 1
            continue
    
    print(f"✅ Processed {len(features_list)} examples")
    if len(features_list) == 0:
        raise ValueError(
            "No usable examples after length filtering. "
            "Lower min_pattern_length or add longer labeled verses."
        )
    if skipped > 0:
        print(f"⚠️  Skipped {skipped} examples")
    if skipped_short > 0:
        print(f"⚠️  Skipped {skipped_short} short patterns (< {min_pattern_length})")
    
    # Convert to DataFrame
    X = pd.DataFrame(features_list)
    y = labels_list
    
    # Class distribution
    class_dist = Counter(y)
    print(f"\n📊 Class Distribution:")
    for label, count in sorted(class_dist.items(), key=lambda x: -x[1]):
        print(f"   {label}: {count} examples")
    
    return X, y


def balance_dataset(
    X: pd.DataFrame,
    y: list,
    random_state: int = 42
) -> tuple[pd.DataFrame, list]:
    """
    Balance classes by upsampling to the max class count.
    """
    df = X.copy()
    df["__label"] = y

    class_counts = df["__label"].value_counts()
    max_count = class_counts.max()

    balanced_parts = []
    for label, count in class_counts.items():
        group = df[df["__label"] == label]
        if count < max_count:
            group = group.sample(max_count, replace=True, random_state=random_state)
        balanced_parts.append(group)

    balanced = pd.concat(balanced_parts, ignore_index=True)
    balanced = balanced.sample(frac=1, random_state=random_state).reset_index(drop=True)

    y_balanced = balanced.pop("__label").tolist()
    X_balanced = balanced

    return X_balanced, y_balanced


def train_advanced_model(
    test_size: float = 0.2,
    random_state: int = 42,
    use_ensemble: bool = True,
    calibrate: bool = True,
    cv_folds: int = 5,
    min_pattern_length: int = 8,
    balance_classes: bool = True
):
    """
    Train advanced model with ensemble learning and confidence calibration.
    
    Args:
        test_size: Proportion of data for testing
        random_state: Random seed for reproducibility
        use_ensemble: Whether to use ensemble of multiple models
        calibrate: Whether to calibrate probabilities
        cv_folds: Cross-validation folds
    
    Returns:
        Trained model, label list, scaler, and metrics
    """
    
    print("=" * 70)
    print("🚀 ADVANCED CHANDAS MODEL TRAINING")
    print("=" * 70)
    
    # Load dataset
    print("\n📂 Building advanced feature dataset...")
    X, y = build_advanced_dataset(
        use_provided_patterns=True,
        min_pattern_length=min_pattern_length
    )
    
    print(f"\n📊 Dataset Statistics:")
    print(f"   Total samples: {len(X)}")
    print(f"   Features: {X.shape[1]}")
    print(f"   Classes: {len(set(y))}")
    print(f"   Feature count: {len(X.columns)}")
    
    # Optional class balancing (upsample)
    if balance_classes:
        print("\n⚖️  Balancing classes with upsampling...")
        X, y = balance_dataset(X, y, random_state=random_state)
        print(f"   Balanced samples: {len(X)}")

    # Feature scaling for better performance
    scaler = StandardScaler()
    X_scaled = pd.DataFrame(
        scaler.fit_transform(X),
        columns=X.columns,
        index=X.index
    )
    
    # Split data
    print(f"\n🔀 Splitting data (test_size={test_size})...")
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    print(f"   Training samples: {len(X_train)}")
    print(f"   Testing samples: {len(X_test)}")
    
    # Build model
    if use_ensemble:
        print(f"\n🌲 Training Ensemble Model (Random Forest + Gradient Boosting)...")

        # Disable early stopping to avoid validation split errors in small datasets
        gb_validation_fraction = 0.1
        gb_n_iter_no_change = None
        
        rf_model = RandomForestClassifier(
            n_estimators=1500,  # Massive increase for maximum accuracy
            max_depth=30,  # Very deep trees
            min_samples_split=2,
            min_samples_leaf=1,
            max_features='sqrt',
            random_state=random_state,
            class_weight='balanced_subsample',
            n_jobs=-1,
            bootstrap=True,
            oob_score=True,
            warm_start=False,
            criterion='gini',
            max_leaf_nodes=None,
            min_impurity_decrease=0.0  # No pruning for max accuracy
        )
        
        gb_model = GradientBoostingClassifier(
            n_estimators=800,  # Very large ensemble
            max_depth=12,  # Deep trees for complex patterns
            learning_rate=0.03,  # Very low for fine-tuned learning
            min_samples_split=2,
            min_samples_leaf=1,
            subsample=0.95,  # Very high subsample
            random_state=random_state,
            validation_fraction=gb_validation_fraction,
            n_iter_no_change=gb_n_iter_no_change,
            max_features='sqrt',
            min_impurity_decrease=0.0
        )
        
        # Voting classifier with RF weighted higher (better for Sanskrit)
        model = VotingClassifier(
            estimators=[
                ('rf', rf_model),
                ('gb', gb_model)
            ],
            voting='soft',
            weights=[2, 1],  # RF weighted 2x more
            n_jobs=-1
        )
        
        print(f"   Components: Random Forest (weight=3) + Gradient Boosting (weight=2)")
        
    else:
        print(f"\n🌲 Training Random Forest Model...")
        model = RandomForestClassifier(
            n_estimators=500,  # Increased
            max_depth=20,
            min_samples_split=3,
            min_samples_leaf=2,
            max_features='sqrt',
            random_state=random_state,
            class_weight='balanced_subsample',
            n_jobs=-1,
            bootstrap=True,
            oob_score=True
        )
    
    # Train model
    model.fit(X_train, y_train)
    print("   ✅ Training complete!")
    
    # Calibrate probabilities if requested
    if calibrate:
        print(f"\n🎯 Calibrating confidence scores with isotonic method...")
        
        # Determine optimal CV folds based on smallest class size
        from collections import Counter
        class_counts = Counter(y_train)
        min_class_count = min(class_counts.values())
        optimal_cv = min(5, min_class_count)  # Use up to 5 folds
        
        if optimal_cv < 2:
            print(f"   ⚠️  Insufficient data for CV calibration (min class: {min_class_count})")
            print(f"   Using isotonic calibration without CV")
            calibrated_model = CalibratedClassifierCV(
                model,
                method='isotonic',
                cv='prefit'
            )
            # Refit on training data
            model.fit(X_train, y_train)
            calibrated_model.fit(X_train, y_train)
        else:
            # Use isotonic instead of sigmoid for less conservative calibration
            print(f"   Using {optimal_cv}-fold CV with isotonic calibration (less conservative)")
            calibrated_model = CalibratedClassifierCV(
                model,
                method='isotonic',  # Changed from sigmoid
                cv=optimal_cv,
                ensemble=True  # Use all CV models for better calibration
            )
            calibrated_model.fit(X_train, y_train)
        
        model = calibrated_model
        print("   ✅ Calibration complete!")
    
    # Cross-validation
    # Adapt CV folds to smallest class size
    from collections import Counter
    min_class_count = min(Counter(y_train).values())
    effective_folds = min(cv_folds, min_class_count)

    if effective_folds < 2:
        print("\n⚠️  Skipping cross-validation (not enough samples per class)")
    else:
        print(f"\n🔄 Performing {effective_folds}-fold stratified cross-validation...")
        skf = StratifiedKFold(n_splits=effective_folds, shuffle=True, random_state=random_state)
    if effective_folds >= 2:
        try:
            cv_scores = cross_val_score(model, X_train, y_train, cv=skf, scoring='accuracy')
            print(f"   CV Accuracy: {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")
        except Exception as e:
            print(f"   ⚠️  CV warning: {e}")
    
    # Evaluate on test set
    print(f"\n📈 Evaluating on test set...")
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)
    
    test_accuracy = accuracy_score(y_test, y_pred)
    test_logloss = log_loss(y_test, y_pred_proba)
    
    print(f"   Test Accuracy: {test_accuracy:.3f}")
    print(f"   Log Loss: {test_logloss:.3f} (lower is better)")
    
    # Confidence analysis
    print(f"\n🎲 Confidence Score Analysis:")
    avg_confidence = np.mean([np.max(probs) for probs in y_pred_proba])
    min_confidence = np.min([np.max(probs) for probs in y_pred_proba])
    max_confidence = np.max([np.max(probs) for probs in y_pred_proba])
    print(f"   Average: {avg_confidence:.3f}")
    print(f"   Min: {min_confidence:.3f}")
    print(f"   Max: {max_confidence:.3f}")
    
    # Feature importance
    importances = None
    feature_names = None
    
    try:
        # Try to extract feature importances from the model
        if hasattr(model, 'feature_importances_'):
            # Direct model
            importances = model.feature_importances_
            feature_names = X.columns
        elif hasattr(model, 'base_estimator'):
            # CalibratedClassifierCV
            base_est = model.base_estimator
            if hasattr(base_est, 'feature_importances_'):
                importances = base_est.feature_importances_
                feature_names = X.columns
            elif hasattr(base_est, 'named_estimators_'):
                # Ensemble inside calibrated
                importances = base_est.named_estimators_['rf'].feature_importances_
                feature_names = X.columns
        elif hasattr(model, 'named_estimators_'):
            # VotingClassifier
            importances = model.named_estimators_['rf'].feature_importances_
            feature_names = X.columns
    except Exception as e:
        print(f"   ⚠️  Could not extract feature importances: {e}")
        importances = None
        feature_names = None
    
    if importances is not None:
        print(f"\n🔍 Top 15 Feature Importance:")
        importance_df = pd.DataFrame({
            'feature': feature_names,
            'importance': importances
        }).sort_values('importance', ascending=False)
        
        for idx, row in importance_df.head(15).iterrows():
            print(f"   {row['feature']:25} {row['importance']:.4f}")
    
    # Classification report
    print(f"\n📊 Classification Report:")
    print(classification_report(y_test, y_pred, zero_division=0))
    
    # Save model
    print(f"\n💾 Saving advanced model...")
    
    base_dir = Path(__file__).resolve().parents[3]
    model_dir = base_dir / "models"
    model_dir.mkdir(exist_ok=True)
    
    model_path = model_dir / "random_forest_enhanced.pkl"
    labels_path = model_dir / "labels_enhanced.pkl"
    scaler_path = model_dir / "scaler_enhanced.pkl"
    metadata_path = model_dir / "model_metadata_enhanced.json"
    
    joblib.dump(model, model_path)
    joblib.dump(sorted(set(y)), labels_path)
    joblib.dump(scaler, scaler_path)
    
    # Save metadata
    metadata = {
        "model_type": "VotingClassifier (RF+GB)" if use_ensemble else "RandomForestClassifier",
        "features": len(X.columns),
        "feature_names": list(X.columns),
        "classes": len(set(y)),
        "class_names": sorted(set(y)),
        "training_samples": len(X_train),
        "test_accuracy": float(test_accuracy),
        "log_loss": float(test_logloss),
        "avg_confidence": float(avg_confidence),
        "calibrated": calibrate,
        "ensemble": use_ensemble,
        "min_pattern_length": min_pattern_length,
        "balance_classes": balance_classes,
        "sklearn_version": "1.8.0",
        "feature_scaling": "StandardScaler"
    }
    
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    print(f"   ✅ Model saved to: {model_path}")
    print(f"   ✅ Labels saved to: {labels_path}")
    print(f"   ✅ Scaler saved to: {scaler_path}")
    print(f"   ✅ Metadata saved to: {metadata_path}")
    
    print("\n" + "=" * 70)
    print("✅ ADVANCED TRAINING COMPLETE!")
    print("=" * 70)
    
    print(f"\n📝 Summary:")
    print(f"   Model: {'Ensemble (RF+GB) with calibration' if use_ensemble and calibrate else 'Single model'}")
    print(f"   Features: {len(X.columns)}")
    print(f"   Test accuracy: {test_accuracy:.1%}")
    print(f"   Average confidence: {avg_confidence:.1%}")
    print(f"   Calibrated: {'Yes' if calibrate else 'No'}")
    
    print(f"\n🎯 Model is ready for deployment!")
    
    return model, sorted(set(y)), scaler, metadata


if __name__ == "__main__":
    train_advanced_model(
        test_size=0.2,
        random_state=42,
        use_ensemble=True,
        calibrate=True,
        cv_folds=5
    )
