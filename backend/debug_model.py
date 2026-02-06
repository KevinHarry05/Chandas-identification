import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.ml.model_loader import model
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import VotingClassifier

print(f"Model type: {type(model)}")
print(f"Has estimator_: {hasattr(model, 'estimator_')}")
print(f"Has base_estimator_: {hasattr(model, 'base_estimator_')}")
attrs = [a for a in dir(model) if 'estimator' in a.lower()]
print(f"Estimator-related attrs: {attrs}")

if isinstance(model, CalibratedClassifierCV):
    est = getattr(model, 'estimator_', None) or getattr(model, 'base_estimator_', None)
    print(f"Extracted estimator: {est}")
    print(f"Extracted estimator type: {type(est)}")
    
    if isinstance(est, VotingClassifier):
        print(f"Has estimators_: {hasattr(est, 'estimators_')}")
        if hasattr(est, 'estimators_'):
            print(f"Number of estimators: {len(est.estimators_)}")
            for i, e in enumerate(est.estimators_):
                print(f"  Estimator {i}: {type(e).__name__}, has estimators_: {hasattr(e, 'estimators_')}")

