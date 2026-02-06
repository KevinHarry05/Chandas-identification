import json

data = json.load(open('data/examples_augmented.json','r',encoding='utf-8'))
examples = data['examples']

print("Sample patterns from training data:")
print("=" * 70)
for ex in examples[:15]:
    meter = ex.get('meter', 'Unknown')
    pattern = ex.get('pattern', '')
    text = ex.get('text', '')[:50]
    print(f"{meter}:")
    print(f"  Pattern: {pattern}")
    print(f"  Text: {text}...")
    print()
