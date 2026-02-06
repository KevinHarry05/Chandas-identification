# backend/app/core/text/laghu_guru.py

import re

# -----------------------------
# Devanagari definitions
# -----------------------------

# Consonants (व्यञ्जन)
CONSONANTS = set("कखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसह")

# Independent vowels (स्वर)
SHORT_VOWELS = {"अ", "इ", "उ", "ऋ", "ऌ"}
LONG_VOWELS = {"आ", "ई", "ऊ", "ॠ", "ए", "ऐ", "ओ", "औ", "ॡ"}

# Dependent vowel signs (मात्राएँ)
SHORT_MATRAS = {"ि", "ु", "ृ", "ॢ"}
LONG_MATRAS = {"ा", "ी", "ू", "ॄ", "े", "ै", "ो", "ौ", "ॣ"}

VOWELS = SHORT_VOWELS | LONG_VOWELS
MATRAS = SHORT_MATRAS | LONG_MATRAS
GURU_MARKS = {"ं", "ः", "ँ"}  # anusvara, visarga, chandrabindu
HALANT = "्"


def is_devanagari(text: str) -> bool:
    return bool(re.search(r"[\u0900-\u097F]", text))


def split_aksharas(text: str):
    """
    Correct akṣara (syllable) segmentation for Sanskrit prosody.
    A syllable is formed by:
    1. Independent vowel, OR
    2. Consonant(s) + vowel matra, OR
    3. Consonant with inherent 'a'
    
    Note: Word-final consonants with halant (virama) are NOT counted as separate syllables.
    They extend the previous syllable to make it Guru.
    """
    aksharas = []
    i = 0
    n = len(text)

    while i < n:
        ch = text[i]

        # Skip whitespace and punctuation
        if ch.isspace() or ch in {",", "।", "॥", ".", ";", ":", "\n", "\r"}:
            i += 1
            continue

        # Skip standalone halant or word-final consonant with halant
        if ch == HALANT:
            # Attach to previous syllable if it exists
            if aksharas:
                aksharas[-1] += ch
            i += 1
            continue

        akshara = ""

        # Independent vowel forms a syllable
        if ch in VOWELS:
            akshara = ch
            i += 1
            # Attach anusvara/visarga if present
            if i < n and text[i] in GURU_MARKS:
                akshara += text[i]
                i += 1
        
        # Consonant starts a syllable
        elif ch in CONSONANTS:
            # Collect consonant cluster (with halants)
            while i < n and text[i] in CONSONANTS:
                akshara += text[i]
                i += 1
                # Check for halant (consonant cluster)
                if i < n and text[i] == HALANT:
                    # Peek ahead - if next is another consonant, it's a cluster
                    if i + 1 < n and text[i + 1] in CONSONANTS:
                        akshara += text[i]
                        i += 1
                    else:
                        # Word-final halant - attach to current syllable and stop
                        akshara += text[i]
                        i += 1
                        break
                else:
                    break
            
            # Attach vowel matra if present
            if i < n and text[i] in MATRAS:
                akshara += text[i]
                i += 1
            
            # Attach anusvara/visarga/chandrabindu
            if i < n and text[i] in GURU_MARKS:
                akshara += text[i]
                i += 1
        
        else:
            # Unknown character, skip
            i += 1
            continue

        if akshara:
            aksharas.append(akshara)

    return aksharas


def classify_akshara(akshara: str) -> str:
    """
    Classify a single akṣara as Laghu (L) or Guru (G)
    
    Guru (G) if:
    - Contains long vowel or long matra
    - Contains anusvara (ं), visarga (ः), or chandrabindu (ँ)
    - Contains halant (consonant cluster)
    
    Laghu (L) if:
    - Contains short vowel or short matra
    - Consonant with inherent short 'a'
    """

    # Guru by anusvara / visarga / chandrabindu
    if any(mark in akshara for mark in GURU_MARKS):
        return "G"

    # Guru by long vowel or long matra
    if any(v in akshara for v in LONG_VOWELS) or any(m in akshara for m in LONG_MATRAS):
        return "G"

    # Guru by consonant cluster (halant present)
    if HALANT in akshara:
        return "G"

    # Laghu by short vowel or short matra
    if any(v in akshara for v in SHORT_VOWELS) or any(m in akshara for m in SHORT_MATRAS):
        return "L"

    # Consonant without explicit matra has inherent short 'a' → Laghu
    if any(c in akshara for c in CONSONANTS):
        return "L"

    # Default to Laghu
    return "L"


def extract_laghu_guru_pattern(verse: str) -> str:
    """
    Main API used by backend.
    Extracts Laghu-Guru pattern from Sanskrit verse.
    """

    if not verse or not is_devanagari(verse):
        raise ValueError("Invalid or non-Devanagari input")

    aksharas = split_aksharas(verse)

    if not aksharas:
        raise ValueError("Laghu–Guru pattern extraction failed")

    pattern = [classify_akshara(a) for a in aksharas]

    return "".join(pattern)
