"""
Quick setup script for Chandas Identifier Backend
Checks dependencies, trains model if needed, and starts server
"""

import sys
import subprocess
from pathlib import Path


def check_python_version():
    """Ensure Python 3.9+"""
    version = sys.version_info
    if version < (3, 9):
        print("❌ Python 3.9+ required")
        print(f"   Current version: {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True


def check_dependencies():
    """Check if requirements are installed"""
    try:
        import fastapi
        import sklearn
        import pandas
        import shap
        print("✅ Core dependencies installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("   Run: pip install -r requirements.txt")
        return False


def check_model_exists():
    """Check if trained model exists"""
    base_dir = Path(__file__).resolve().parents[1]
    model_path = base_dir / "models" / "random_forest.pkl"
    
    if model_path.exists():
        print(f"✅ Model found: {model_path}")
        return True
    else:
        print(f"⚠️  Model not found: {model_path}")
        return False


def train_model():
    """Train the model"""
    print("\n🚀 Starting model training...")
    print("   This may take a few minutes...\n")
    
    try:
        subprocess.run([
            sys.executable, "-m",
            "backend.app.core.ml.train_full_model"
        ], check=True)
        print("\n✅ Model training complete!")
        return True
    except subprocess.CalledProcessError:
        print("\n❌ Model training failed")
        return False


def start_server():
    """Start the FastAPI server"""
    print("\n🚀 Starting server...")
    print("   API will be available at: http://localhost:8000")
    print("   Docs available at: http://localhost:8000/docs")
    print("   Press Ctrl+C to stop\n")
    
    subprocess.run([
        sys.executable, "-m", "uvicorn",
        "backend.app.main:app",
        "--reload",
        "--host", "0.0.0.0",
        "--port", "8000"
    ])


def main():
    print("=" * 70)
    print("🎯 CHANDAS IDENTIFIER - BACKEND SETUP")
    print("=" * 70)
    print()
    
    # Check Python version
    if not check_python_version():
        return 1
    
    # Check dependencies
    if not check_dependencies():
        return 1
    
    # Check model
    if not check_model_exists():
        response = input("\n⚠️  Model not found. Train now? (y/n): ")
        if response.lower() == 'y':
            if not train_model():
                return 1
        else:
            print("❌ Cannot start server without trained model")
            print("   Run: python -m backend.app.core.ml.train_full_model")
            return 1
    
    print("\n" + "=" * 70)
    print("✅ SETUP COMPLETE - STARTING SERVER")
    print("=" * 70)
    
    # Start server
    start_server()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
