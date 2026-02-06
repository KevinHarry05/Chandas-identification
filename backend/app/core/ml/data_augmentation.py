"""
Data Augmentation for Sanskrit Meter Classification
Generates synthetic training examples by pattern permutation and variation
"""
import json
from typing import List, Dict, Tuple
import random
from collections import Counter
import numpy as np


def load_dataset(filepath: str) -> List[Dict]:
    """Load examples from JSON file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['examples']


def remove_duplicates(examples: List[Dict]) -> List[Dict]:
    """Remove duplicate texts while preserving unique examples"""
    seen = set()
    unique = []
    for ex in examples:
        text_hash = ex['text'].strip()
        if text_hash not in seen:
            seen.add(text_hash)
            unique.append(ex)
    return unique


def augment_by_pattern_variation(examples: List[Dict], target_count: int = 30) -> List[Dict]:
    """
    Augment data by creating variations based on patterns
    For each meter/pattern combination, create synthetic examples
    """
    augmented = []
    
    # Group by meter
    by_meter = {}
    for ex in examples:
        meter = ex['meter']
        if meter not in by_meter:
            by_meter[meter] = []
        by_meter[meter].append(ex)
    
    for meter, meter_examples in by_meter.items():
        current_count = len(meter_examples)
        
        if current_count < target_count:
            needed = target_count - current_count
            
            # Create synthetic examples by replication with minor variations
            for i in range(needed):
                base_ex = meter_examples[i % len(meter_examples)]
                
                # Create synthetic example (keeping same pattern and meter)
                synthetic = {
                    'text': base_ex['text'],  # In production, would generate new text
                    'meter': base_ex['meter'],
                    'topic': random.choice(['धर्मः', 'प्रकृतिः', 'ज्ञानम्', 'भक्तिः', 'प्रेम']),
                    'pattern': base_ex['pattern'],
                    'source': 'Augmented'
                }
                augmented.append(synthetic)
    
    return augmented


def balance_dataset(examples: List[Dict], target_per_class: int = 30) -> List[Dict]:
    """
    Balance dataset by oversampling minority classes
    """
    by_meter = {}
    for ex in examples:
        meter = ex['meter']
        if meter not in by_meter:
            by_meter[meter] = []
        by_meter[meter].append(ex)
    
    balanced = []
    
    for meter, meter_examples in by_meter.items():
        # Add all original examples
        balanced.extend(meter_examples)
        
        # If class has fewer than target, oversample
        current_count = len(meter_examples)
        if current_count < target_per_class:
            needed = target_per_class - current_count
            
            # Oversample with replacement
            oversampled = random.choices(meter_examples, k=needed)
            for i, ex in enumerate(oversampled):
                synthetic = ex.copy()
                synthetic['source'] = f'Oversampled_{i}'
                balanced.append(synthetic)
    
    return balanced


def create_pattern_noise(pattern: str, noise_prob: float = 0.1) -> str:
    """
    Add noise to pattern for robustness training
    Randomly flip L<->G with low probability
    """
    if random.random() > noise_prob:
        return pattern
    
    chars = list(pattern)
    # Flip one random position
    if chars:
        idx = random.randint(0, len(chars) - 1)
        if chars[idx] == 'L':
            chars[idx] = 'G'
        elif chars[idx] == 'G':
            chars[idx] = 'L'
    
    return ''.join(chars)


def augment_dataset(
    input_file: str,
    output_file: str,
    target_per_class: int = 30,
    add_pattern_noise: bool = False
) -> Tuple[int, int]:
    """
    Main augmentation pipeline
    
    Returns:
        (original_count, augmented_count)
    """
    print("📂 Loading dataset...")
    examples = load_dataset(input_file)
    original_count = len(examples)
    print(f"   Loaded {original_count} examples")
    
    print("🧹 Removing duplicates...")
    unique_examples = remove_duplicates(examples)
    unique_count = len(unique_examples)
    print(f"   {unique_count} unique examples ({original_count - unique_count} duplicates removed)")
    
    print(f"⚖️  Balancing dataset (target: {target_per_class} per class)...")
    balanced = balance_dataset(unique_examples, target_per_class)
    balanced_count = len(balanced)
    print(f"   {balanced_count} examples after balancing")
    
    # Add pattern noise if requested (for robustness)
    if add_pattern_noise:
        print("🔊 Adding pattern noise for robustness...")
        noisy_count = 0
        for ex in balanced:
            if ex.get('source', '').startswith('Oversampled'):
                ex['pattern'] = create_pattern_noise(ex['pattern'], 0.05)
                noisy_count += 1
        print(f"   Added noise to {noisy_count} oversampled examples")
    
    # Count final distribution
    meter_counts = Counter(ex['meter'] for ex in balanced)
    print("\n📊 Final distribution:")
    for meter, count in sorted(meter_counts.items()):
        print(f"   {meter}: {count}")
    
    # Save augmented dataset
    print(f"\n💾 Saving augmented dataset to {output_file}...")
    output_data = {'examples': balanced}
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Augmentation complete!")
    print(f"   Original: {original_count} → Unique: {unique_count} → Augmented: {balanced_count}")
    print(f"   Increase: {balanced_count - original_count} examples ({(balanced_count/original_count - 1)*100:.1f}% growth)")
    
    return original_count, balanced_count


if __name__ == "__main__":
    input_path = "data/examples.json"
    output_path = "data/examples_augmented.json"
    
    augment_dataset(
        input_file=input_path,
        output_file=output_path,
        target_per_class=30,  # Target 30 examples per meter
        add_pattern_noise=False  # Disable noise for now
    )
