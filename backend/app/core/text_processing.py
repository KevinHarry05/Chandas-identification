# backend/app/core/text_processing.py

# ⚠️ DEPRECATED: This file contains duplicate pattern extraction logic.
# ✅ Use backend.app.core.text.laghu_guru.extract_laghu_guru_pattern() instead.

# This file is kept for backward compatibility only.
# All new code should import from app.core.text.laghu_guru

from .text.laghu_guru import extract_laghu_guru_pattern as _extract_pattern


def analyze_sanskrit_verse(verse: str) -> dict:
    """
    Analyze Sanskrit verse (delegates to laghu_guru.py).
    
    ⚠️ DEPRECATED: Use laghu_guru.extract_laghu_guru_pattern() directly.
    """
    lg = _extract_pattern(verse)

    guru_count = lg.count("G")
    laghu_count = lg.count("L")
    length = len(lg)

    ratio = round(guru_count / laghu_count, 3) if laghu_count else 0

    return {
        "laghu_guru_pattern": lg,
        "pattern_length": length,
        "guru_count": guru_count,
        "laghu_count": laghu_count,
        "guru_laghu_ratio": ratio,
    }


# Alias for backward compatibility
extract_laghu_guru_pattern = _extract_pattern

