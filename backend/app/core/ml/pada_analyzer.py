# ============================================================
# Pāda Analyzer
# ============================================================

from .sanskrit_prosody import syllabify_sanskrit


def pada_syllable_lengths(verse: str):
    """
    Estimate syllable (akṣara) count per pāda.

    Assumptions:
    - Verse may be a half-śloka or full śloka
    - We split pādas using danda markers or spaces as fallback
    """

    verse = verse.strip()
    if not verse:
        return []

    # Sanskrit danda markers
    if "।" in verse:
        padas = [p.strip() for p in verse.split("।") if p.strip()]
    else:
        # Fallback: split roughly into 4 parts by words
        words = verse.split()
        if len(words) < 4:
            padas = [verse]
        else:
            size = max(1, len(words) // 4)
            padas = [
                " ".join(words[i:i + size])
                for i in range(0, len(words), size)
            ]

    lengths = []
    for pada in padas:
        aksharas = syllabify_sanskrit(pada)
        lengths.append(len(aksharas))

    return lengths
