"""Test the corrected Laghu-Guru pattern extraction"""

from app.core.text.laghu_guru import extract_laghu_guru_pattern, split_aksharas

# Test verse
verse = """धर्मो रक्षति रक्षितः
सत्यं वदति सर्वदा।
ज्ञानं ददाति विनयं
विद्या ददाति पात्रताम्॥"""

print("=" * 60)
print("Testing Laghu-Guru Pattern Extraction")
print("=" * 60)

print(f"\nVerse:\n{verse}\n")

# Split into aksharas (syllables)
aksharas = split_aksharas(verse)
print(f"Syllables (aksharas): {len(aksharas)}")
print(f"Aksharas: {aksharas}\n")

# Extract pattern
pattern = extract_laghu_guru_pattern(verse)
print(f"Pattern: {pattern}")
print(f"Pattern Length: {len(pattern)}")
print(f"Guru (G): {pattern.count('G')}")
print(f"Laghu (L): {pattern.count('L')}")

print("\n" + "=" * 60)
print("Expected: LLGLGLLG pattern (Anuṣṭubh meter)")
print("=" * 60)

# Test individual lines
lines = [
    "धर्मो रक्षति रक्षितः",
    "सत्यं वदति सर्वदा",
    "ज्ञानं ददाति विनयं",
    "विद्या ददाति पात्रताम्"
]

print("\nPer-line analysis:")
for line in lines:
    line_pattern = extract_laghu_guru_pattern(line)
    print(f"{line:30} → {line_pattern}")
