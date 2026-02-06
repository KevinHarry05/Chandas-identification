# ============================================================
# ML Model Training with Full Dataset (NO HARDCODING)
# ============================================================

import joblib
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import numpy as np

from app.core.ml.load_full_data import build_dataset_from_json


def train_chandas_model(
    test_size: float = 0.2,
    random_state: int = 42,
    n_estimators: int = 200,
    max_depth: int = 20,
    min_samples_split: int = 5,
    min_samples_leaf: int = 2,
    cv_folds: int = 5
):
    """
    Train Random Forest classifier on full dataset with validation.
    
    Args:
        test_size: Proportion of data for testing
        random_state: Random seed for reproducibility
        n_estimators: Number of trees in forest
        max_depth: Maximum tree depth
        min_samples_split: Minimum samples to split node
        min_samples_leaf: Minimum samples in leaf
        cv_folds: Cross-validation folds
    
    Returns:
        Trained model, label list, and metrics
    """
    
    print("=" * 70)
    print("🚀 CHANDAS MODEL TRAINING - FULL DATASET")
    print("=" * 70)
    
    # Load dataset
    print("\n📂 Loading dataset from examples.json...")
    X, y = build_dataset_from_json(use_provided_patterns=False)
    
    print(f"\n📊 Dataset Statistics:")
    print(f"   Total samples: {len(X)}")
    print(f"   Features: {X.shape[1]}")
    print(f"   Classes: {len(set(y))}")
    print(f"   Feature names: {list(X.columns)}")
    
    # Split data
    print(f"\n🔀 Splitting data (test_size={test_size})...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    print(f"   Training samples: {len(X_train)}")
    print(f"   Testing samples: {len(X_test)}")
    
    # Initialize model
    print(f"\n🌲 Training Random Forest...")
    print(f"   n_estimators: {n_estimators}")
    print(f"   max_depth: {max_depth}")
    print(f"   min_samples_split: {min_samples_split}")
    print(f"   min_samples_leaf: {min_samples_leaf}")
    
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        min_samples_leaf=min_samples_leaf,
        random_state=random_state,
        class_weight='balanced',  # Handle class imbalance
        n_jobs=-1  # Use all CPU cores
    )
    
    model.fit(X_train, y_train)
    print("   ✅ Training complete!")
    
    # Cross-validation
    print(f"\n🔄 Performing {cv_folds}-fold cross-validation...")
    cv_scores = cross_val_score(model, X_train, y_train, cv=cv_folds, scoring='accuracy')
    print(f"   CV Accuracy: {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")
    
    # Evaluate on test set
    print(f"\n📈 Evaluating on test set...")
    y_pred = model.predict(X_test)
    test_accuracy = accuracy_score(y_test, y_pred)
    print(f"   Test Accuracy: {test_accuracy:.3f}")
    
    # Feature importance
    print(f"\n🔍 Feature Importance:")
    importances = model.feature_importances_
    for feature, importance in zip(X.columns, importances):
        print(f"   {feature}: {importance:.4f}")
    
    # Classification report
    print(f"\n📊 Classification Report:")
    print(classification_report(y_test, y_pred, zero_division=0))
    
    # Get unique labels in sorted order
    unique_labels = sorted(set(y))
    
    # Save model
    print(f"\n💾 Saving model...")
    BASE_DIR = Path(__file__).resolve().parents[3]
    MODEL_DIR = BASE_DIR / "models"
    MODEL_DIR.mkdir(exist_ok=True)
    
    MODEL_PATH = MODEL_DIR / "random_forest.pkl"
    LABELS_PATH = MODEL_DIR / "labels.pkl"
    
    joblib.dump(model, MODEL_PATH)
    joblib.dump(unique_labels, LABELS_PATH)
    
    print(f"   ✅ Model saved to: {MODEL_PATH}")
    print(f"   ✅ Labels saved to: {LABELS_PATH}")
    
    # Save training metadata
    metadata = {
        "total_samples": len(X),
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "num_classes": len(unique_labels),
        "classes": unique_labels,
        "test_accuracy": float(test_accuracy),
        "cv_accuracy_mean": float(cv_scores.mean()),
        "cv_accuracy_std": float(cv_scores.std()),
        "feature_names": list(X.columns),
        "feature_importance": {
            feature: float(importance) 
            for feature, importance in zip(X.columns, importances)
        },
        "hyperparameters": {
            "n_estimators": n_estimators,
            "max_depth": max_depth,
            "min_samples_split": min_samples_split,
            "min_samples_leaf": min_samples_leaf,
            "random_state": random_state
        }
    }
    
    METADATA_PATH = MODEL_DIR / "model_metadata.json"
    import json
    with open(METADATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    print(f"   ✅ Metadata saved to: {METADATA_PATH}")
    
    print("\n" + "=" * 70)
    print("✅ TRAINING COMPLETE!")
    print("=" * 70)
    
    return model, unique_labels, {
        "test_accuracy": test_accuracy,
        "cv_scores": cv_scores,
        "y_test": y_test,
        "y_pred": y_pred
    }


if __name__ == "__main__":
    # Train model with full dataset
    model, labels, metrics = train_chandas_model()
    
    print(f"\n📝 Summary:")
    print(f"   Model trained on {len(labels)} chandas types")
    print(f"   Test accuracy: {metrics['test_accuracy']:.1%}")
    print(f"\n🎯 Model is ready for deployment!")
