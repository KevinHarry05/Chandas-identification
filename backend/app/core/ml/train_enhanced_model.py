# ============================================================
# Enhanced Training with Advanced Features & Optimization
# ============================================================

import joblib
import json
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import classification_report, accuracy_score
import numpy as np

from app.core.ml.load_full_data import load_examples_json
from app.core.ml.enhanced_features import extract_enhanced_features
from app.core.text.laghu_guru import extract_laghu_guru_pattern
import pandas as pd


def build_enhanced_dataset(json_path=None, use_provided_patterns=True):
    """
    Build dataset with enhanced features.
    """
    examples = load_examples_json(json_path)
    
    print(f"📚 Loaded {len(examples)} examples from JSON")
    
    features_list = []
    labels_list = []
    skipped = 0
    
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
            
            # Extract enhanced features
            features = extract_enhanced_features(pattern)
            features_list.append(features)
            labels_list.append(meter)
        
        except Exception as e:
            print(f"⚠️  Skipping example {idx}: {e}")
            skipped += 1
            continue
    
    print(f"✅ Processed {len(features_list)} examples")
    if skipped > 0:
        print(f"⚠️  Skipped {skipped} examples")
    
    X = pd.DataFrame(features_list)
    
    # Filter classes with at least 2 examples
    class_counts = pd.Series(labels_list).value_counts()
    valid_classes = class_counts[class_counts >= 2].index.tolist()
    
    if len(valid_classes) < len(class_counts):
        print(f"⚠️  Filtering classes with < 2 examples")
        mask = [label in valid_classes for label in labels_list]
        X = X[mask].reset_index(drop=True)
        labels_list = [label for label, keep in zip(labels_list, mask) if keep]
    
    print("\n📊 Class Distribution:")
    for meter, count in pd.Series(labels_list).value_counts().items():
        print(f"   {meter}: {count} examples")
    
    return X, labels_list


def train_optimized_model(
    test_size=0.2,
    random_state=42,
    optimize_hyperparameters=True
):
    """
    Train model with enhanced features and hyperparameter optimization.
    """
    
    print("=" * 70)
    print("🚀 ENHANCED CHANDAS MODEL TRAINING")
    print("=" * 70)
    
    # Load dataset with enhanced features
    print("\n📂 Building enhanced feature dataset...")
    X, y = build_enhanced_dataset(use_provided_patterns=False)
    
    print(f"\n📊 Dataset Statistics:")
    print(f"   Total samples: {len(X)}")
    print(f"   Features: {X.shape[1]}")
    print(f"   Classes: {len(set(y))}")
    print(f"\n   Feature names: {list(X.columns[:5])}... (showing first 5)")
    
    # Split data
    print(f"\n🔀 Splitting data (test_size={test_size})...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    print(f"   Training samples: {len(X_train)}")
    print(f"   Testing samples: {len(X_test)}")
    
    if optimize_hyperparameters:
        print(f"\n🔧 Optimizing hyperparameters with GridSearchCV...")
        
        # Define parameter grid
        param_grid = {
            'n_estimators': [100, 200, 300],
            'max_depth': [10, 20, 30, None],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4],
            'max_features': ['sqrt', 'log2', None]
        }
        
        # Grid search with cross-validation
        rf_base = RandomForestClassifier(random_state=random_state, class_weight='balanced', n_jobs=-1)
        
        grid_search = GridSearchCV(
            rf_base,
            param_grid,
            cv=3,
            scoring='accuracy',
            n_jobs=-1,
            verbose=1
        )
        
        grid_search.fit(X_train, y_train)
        
        model = grid_search.best_estimator_
        
        print(f"\n✅ Best parameters found:")
        for param, value in grid_search.best_params_.items():
            print(f"   {param}: {value}")
        print(f"   Best CV score: {grid_search.best_score_:.3f}")
    
    else:
        # Use good default parameters
        print(f"\n🌲 Training Random Forest with enhanced features...")
        model = RandomForestClassifier(
            n_estimators=300,
            max_depth=30,
            min_samples_split=2,
            min_samples_leaf=1,
            max_features='sqrt',
            random_state=random_state,
            class_weight='balanced',
            n_jobs=-1
        )
        model.fit(X_train, y_train)
        print("   ✅ Training complete!")
    
    # Cross-validation
    print(f"\n🔄 Performing 5-fold cross-validation...")
    cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
    print(f"   CV Accuracy: {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")
    
    # Evaluate on test set
    print(f"\n📈 Evaluating on test set...")
    y_pred = model.predict(X_test)
    test_accuracy = accuracy_score(y_test, y_pred)
    print(f"   Test Accuracy: {test_accuracy:.3f}")
    
    # Feature importance (top 10)
    print(f"\n🔍 Top 10 Feature Importance:")
    importances = model.feature_importances_
    feature_importance = sorted(
        zip(X.columns, importances),
        key=lambda x: x[1],
        reverse=True
    )
    for feature, importance in feature_importance[:10]:
        print(f"   {feature:25} {importance:.4f}")
    
    # Classification report
    print(f"\n📊 Classification Report:")
    print(classification_report(y_test, y_pred, zero_division=0))
    
    # Save model
    print(f"\n💾 Saving enhanced model...")
    BASE_DIR = Path(__file__).resolve().parents[3]
    MODEL_DIR = BASE_DIR / "models"
    MODEL_DIR.mkdir(exist_ok=True)
    
    MODEL_PATH = MODEL_DIR / "random_forest_enhanced.pkl"
    LABELS_PATH = MODEL_DIR / "labels_enhanced.pkl"
    
    unique_labels = sorted(set(y))
    
    joblib.dump(model, MODEL_PATH)
    joblib.dump(unique_labels, LABELS_PATH)
    
    print(f"   ✅ Model saved to: {MODEL_PATH}")
    print(f"   ✅ Labels saved to: {LABELS_PATH}")
    
    # Save metadata
    metadata = {
        "total_samples": len(X),
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "num_classes": len(unique_labels),
        "classes": unique_labels,
        "num_features": X.shape[1],
        "feature_names": list(X.columns),
        "test_accuracy": float(test_accuracy),
        "cv_accuracy_mean": float(cv_scores.mean()),
        "cv_accuracy_std": float(cv_scores.std()),
        "feature_importance": {
            feature: float(importance) 
            for feature, importance in feature_importance[:20]
        },
        "model_type": "RandomForest_Enhanced",
        "optimization": "GridSearchCV" if optimize_hyperparameters else "Default"
    }
    
    METADATA_PATH = MODEL_DIR / "model_metadata_enhanced.json"
    with open(METADATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    print(f"   ✅ Metadata saved to: {METADATA_PATH}")
    
    print("\n" + "=" * 70)
    print("✅ ENHANCED TRAINING COMPLETE!")
    print("=" * 70)
    
    return model, unique_labels, {
        "test_accuracy": test_accuracy,
        "cv_scores": cv_scores,
        "feature_importance": feature_importance
    }


if __name__ == "__main__":
    # Train with hyperparameter optimization
    print("Training with hyperparameter optimization...")
    print("This may take several minutes...\n")
    
    model, labels, metrics = train_optimized_model(optimize_hyperparameters=True)
    
    print(f"\n📝 Summary:")
    print(f"   Model trained on {len(labels)} chandas types")
    print(f"   Test accuracy: {metrics['test_accuracy']:.1%}")
    print(f"   Features used: {len(metrics['feature_importance'])}")
    print(f"\n🎯 Enhanced model ready for deployment!")
