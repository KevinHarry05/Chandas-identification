# ============================================================
# Full Dataset Loader for Chandas Training (NO HARDCODING)
# ============================================================

import json
import pandas as pd
from pathlib import Path
from typing import Tuple, List, Dict
from ..text.laghu_guru import extract_laghu_guru_pattern


def load_examples_json(json_path: Path = None) -> List[Dict]:
    """
    Load examples from JSON file.
    
    Args:
        json_path: Path to examples.json (auto-detected if None)
    
    Returns:
        List of example dictionaries
    """
    if json_path is None:
        # Auto-detect path from project structure
        current_file = Path(__file__).resolve()
        # Navigate up: load_full_data.py -> ml -> core -> app -> backend -> chandas_project
        backend_dir = current_file.parents[3]  # Navigate to backend/
        project_root = backend_dir.parent  # Navigate to chandas_project
        json_path = project_root / "data" / "examples.json"
    else:
        # Convert to Path if string
        json_path = Path(json_path) if isinstance(json_path, str) else json_path
    
    if not json_path.exists():
        raise FileNotFoundError(f"Examples file not found: {json_path}")
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if 'examples' not in data:
        raise ValueError("JSON must contain 'examples' key")
    
    return data['examples']


def extract_features_from_pattern(pattern: str) -> Dict[str, float]:
    """
    Extract numerical features from Laghu-Guru pattern.
    
    Args:
        pattern: String of L and G characters
    
    Returns:
        Dictionary of features
    """
    if not pattern or not isinstance(pattern, str):
        raise ValueError("Invalid pattern")
    
    pattern_length = len(pattern)
    guru_count = pattern.count("G")
    laghu_count = pattern.count("L")
    
    # Prevent division by zero
    guru_laghu_ratio = (
        guru_count / laghu_count if laghu_count > 0 else float(guru_count)
    )
    
    return {
        "pattern_length": float(pattern_length),
        "guru_count": float(guru_count),
        "laghu_count": float(laghu_count),
        "guru_laghu_ratio": float(guru_laghu_ratio),
    }


def build_dataset_from_json(
    json_path: Path = None,
    use_provided_patterns: bool = True,
    min_examples_per_class: int = 2
) -> Tuple[pd.DataFrame, List[str]]:
    """
    Build complete training dataset from examples.json.
    
    Args:
        json_path: Path to JSON file
        use_provided_patterns: If True, use 'pattern' field from JSON.
                              If False, extract pattern from 'text' field.
        min_examples_per_class: Minimum examples required per chandas type
    
    Returns:
        Tuple of (features_df, labels_list)
    """
    examples = load_examples_json(json_path)
    
    if len(examples) == 0:
        raise ValueError("No examples found in JSON file")
    
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
            
            # Get pattern from JSON or extract from text
            if use_provided_patterns and 'pattern' in example:
                pattern = example['pattern']
            elif 'text' in example:
                pattern = extract_laghu_guru_pattern(example['text'])
            else:
                skipped += 1
                continue
            
            # Extract features
            features = extract_features_from_pattern(pattern)
            features_list.append(features)
            labels_list.append(meter)
        
        except Exception as e:
            print(f"⚠️  Skipping example {idx}: {e}")
            skipped += 1
            continue
    
    if len(features_list) == 0:
        raise ValueError("No valid examples could be processed")
    
    print(f"✅ Successfully processed {len(features_list)} examples")
    if skipped > 0:
        print(f"⚠️  Skipped {skipped} invalid examples")
    
    # Convert to DataFrame
    X = pd.DataFrame(features_list)
    
    # Filter classes with insufficient examples
    class_counts = pd.Series(labels_list).value_counts()
    valid_classes = class_counts[class_counts >= min_examples_per_class].index.tolist()
    
    if len(valid_classes) < len(class_counts):
        print(f"⚠️  Filtering classes with < {min_examples_per_class} examples")
        mask = [label in valid_classes for label in labels_list]
        X = X[mask].reset_index(drop=True)
        labels_list = [label for label, keep in zip(labels_list, mask) if keep]
        print(f"✅ Kept {len(valid_classes)} classes with sufficient data")
    
    # Print class distribution
    print("\n📊 Class Distribution:")
    for meter, count in pd.Series(labels_list).value_counts().items():
        print(f"   {meter}: {count} examples")
    
    return X, labels_list


if __name__ == "__main__":
    # Test data loading
    X, y = build_dataset_from_json()
    print(f"\n✅ Dataset Shape: {X.shape}")
    print(f"✅ Number of Classes: {len(set(y))}")
    print(f"✅ Features: {list(X.columns)}")
