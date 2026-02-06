#!/usr/bin/env python
"""
Generate training data with pattern subsequences for better short-pattern recognition
"""

import json
from pathlib import Path
from collections import defaultdict

# Load existing data
aug_path = Path("data/examples_augmented.json")
with open(aug_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

original_examples = data['examples']

# Generate subsequence examples
new_examples = []
min_length = 8
max_length = 20

for ex in original_examples:
    meter = ex.get('meter')
    pattern = ex.get('pattern', '')
    
    if len(pattern) < min_length:
        continue
    
    # Add original
    new_examples.append(ex)
    
    # Generate subsequences if pattern is long enough
    if len(pattern) >= 16:
        # Start subsequence (first half)
        start_sub = pattern[:min(16, len(pattern)//2)]
        if len(start_sub) >= min_length:
            new_examples.append({
                'text': ex.get('text', '')[:30] + '...',
                'meter': meter,
                'pattern': start_sub,
                'topic': ex.get('topic', ''),
                'source': 'Subsequence_Start'
            })
        
        # Middle subsequence
        if len(pattern) >= 24:
            mid_point = len(pattern) // 2
            mid_sub = pattern[mid_point-8:mid_point+8]
            if len(mid_sub) >= min_length:
                new_examples.append({
                    'text': '...' + ex.get('text', '')[20:50] + '...',
                    'meter': meter,
                    'pattern': mid_sub,
                    'topic': ex.get('topic', ''),
                    'source': 'Subsequence_Mid'
                })
        
        # End subsequence (last half)
        end_sub = pattern[-min(16, len(pattern)//2):]
        if len(end_sub) >= min_length:
            new_examples.append({
                'text': '...' + ex.get('text', '')[-30:],
                'meter': meter,
                'pattern': end_sub,
                'topic': ex.get('topic', ''),
                'source': 'Subsequence_End'
            })

# Save expanded data
expanded_data = {'examples': new_examples}
with open(aug_path, 'w', encoding='utf-8') as f:
    json.dump(expanded_data, f, ensure_ascii=False, indent=2)

print(f"✅ Generated {len(new_examples)} examples (from {len(original_examples)} originals)")
print(f"   Added {len(new_examples) - len(original_examples)} subsequence examples")

# Count by meter
from collections import Counter
meter_counts = Counter([ex['meter'] for ex in new_examples])
print(f"\n📊 Distribution:")
for meter, count in sorted(meter_counts.items(), key=lambda x: -x[1]):
    print(f"   {meter}: {count}")
