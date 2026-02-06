#!/usr/bin/env python
"""
Standalone script to retrain the Chandas model with improved hyperparameters
"""

import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from app.core.ml.train_advanced_model import train_advanced_model

if __name__ == "__main__":
    print("🚀 Starting model retraining with improved hyperparameters...")
    print("=" * 70)
    
    # Train with optimized settings - NO CALIBRATION for higher confidence
    model, labels, scaler, metrics = train_advanced_model(
        test_size=0.15,  # Smaller test set for more training data
        random_state=42,
        use_ensemble=True,
        calibrate=False,  # DISABLE calibration to get raw high confidences
        cv_folds=5,
        min_pattern_length=8,
        balance_classes=True
    )
    
    print("\n" + "=" * 70)
    print("✅ Model retraining complete!")
    print(f"📊 Test Accuracy: {metrics['test_accuracy']:.2%}")
    print(f"📁 Model saved to: {metrics['model_path']}")
    print("=" * 70)
    print("\n⚠️  Please restart the backend server to load the new model")
