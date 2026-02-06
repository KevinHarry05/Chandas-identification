# ============================================================
# Deterministic Akṣara-based Sanskrit Prosody (Paninian-lite)
# ============================================================

# --- Unicode character sets ---

VOWELS = set("अआइईउऊऋॠऌॡएऐओऔ")

# Vowel signs (mātrās)
VOWEL_SIGNS = set("ािीुूृॄेैोौ")

CONSONANTS = set(
    "कखगघङ"
    "चछजझञ"
    "टठडढण"
    "तथदधन"
    "पफबभम"
    "यरलव"
    "शषसह"
)

HALANT = "्"
ANUSVARA = "ं"
VISARGA = "ः"

LONG_VOWELS = set("आईऊॠएऐओऔ")
LONG_VOWEL_SIGNS = set("ाीूॄेैोौ")


# ============================================================
# Akṣara (syllable) segmentation — REFINED
# ============================================================

def akshara_split(word: str):
    """
    Split a Devanāgarī word into akṣaras using deterministic rules.

    Refinement:
    - A vowel sign (mātrā) CLOSES the akṣara formed by the immediately
      preceding consonant cluster.
    - Do NOT allow vowel signs to absorb following consonants.
    """
    aksharas = []
    cluster = ""   # builds consonant cluster
    nucleus = ""   # vowel or vowel sign + diacritics

    i = 0
    n = len(word)

    while i < n:
        ch = word[i]

        # Build consonant cluster (including halant)
        if ch in CONSONANTS or ch == HALANT:
            # If we already have a completed nucleus, flush previous akṣara
            if nucleus:
                aksharas.append(cluster + nucleus)
                cluster = ""
                nucleus = ""

            cluster += ch
            i += 1
            continue

        # Independent vowel → nucleus
        if ch in VOWELS:
            nucleus = ch

            # Attach anusvāra / visarga
            if i + 1 < n and word[i + 1] in (ANUSVARA, VISARGA):
                nucleus += word[i + 1]
                i += 1

            aksharas.append(cluster + nucleus)
            cluster = ""
            nucleus = ""
            i += 1
            continue

        # Vowel sign (mātrā) → nucleus for current cluster
        if ch in VOWEL_SIGNS:
            nucleus = ch

            # Attach anusvāra / visarga
            if i + 1 < n and word[i + 1] in (ANUSVARA, VISARGA):
                nucleus += word[i + 1]
                i += 1

            aksharas.append(cluster + nucleus)
            cluster = ""
            nucleus = ""
            i += 1
            continue

        # Anusvāra / Visarga without explicit vowel (edge cases)
        if ch in (ANUSVARA, VISARGA):
            # Attach to previous akṣara if exists
            if aksharas:
                aksharas[-1] += ch
            i += 1
            continue

        # Any other character (punctuation etc.)
        i += 1

    # Flush any remaining cluster (edge case)
    if cluster:
        aksharas.append(cluster)

    return aksharas


def syllabify_sanskrit(text: str):
    """
    Akṣara-level syllabification for a Sanskrit verse.
    """
    text = text.strip()
    if not text:
        return []

    syllables = []
    for token in text.split():
        syllables.extend(akshara_split(token))

    return syllables


# ============================================================
# Laghu / Guru classification
# ============================================================

def is_guru(akshara: str) -> bool:
    """
    Guru if:
    - Long vowel or long vowel sign present
    - Anusvāra or Visarga present
    """
    for ch in akshara:
        if ch in LONG_VOWELS or ch in LONG_VOWEL_SIGNS:
            return True
        if ch in (ANUSVARA, VISARGA):
            return True
    return False


def verse_to_pattern(verse: str) -> str:
    """
    Convert Sanskrit verse → Laghu/Guru pattern.
    """
    aksharas = syllabify_sanskrit(verse)
    return "".join("G" if is_guru(a) else "L" for a in aksharas)
