def rerank_predictions(predictions, pattern_length, pada_lengths=None):
    """
    Hybrid re-ranking using:
    - ML confidence
    - Optional pāda-level feasibility
    - Śloka-level structural heuristic (Phase 6)
    """

    adjusted = []

    # ----------------------------
    # Compute averages if available
    # ----------------------------
    avg_pada = None
    if pada_lengths is not None and len(pada_lengths) > 0:
        avg_pada = sum(pada_lengths) / len(pada_lengths)

    total_syllables = pattern_length

    for item in predictions:
        chandas = item["chandas"]
        confidence = float(item["confidence"])

        # =================================================
        # PHASE 5: Pāda-aware soft constraints (if known)
        # =================================================

        # Anuṣṭubh: ~8 syllables per pāda
        if chandas == "अनुष्टुभ्" and avg_pada is not None:
            if 7 <= avg_pada <= 9:
                confidence += 0.15
            else:
                confidence -= 0.05

        # Vasantatilakā: long (~14 per pāda)
        if chandas == "वसन्ततिलका" and avg_pada is not None:
            if avg_pada < 10:
                confidence -= 0.20

        # Indravajrā: ~11 per pāda
        if chandas == "इन्द्रवज्रा" and avg_pada is not None:
            if 10 <= avg_pada <= 12:
                confidence += 0.05

        # =================================================
        # PHASE 6: Śloka-level heuristic (NEW)
        # =================================================

        # If pāda structure is unknown but total syllables
        # resemble a śloka (~28–36), gently favor Anuṣṭubh
        if avg_pada is None:
            if chandas == "अनुष्टुभ्" and 28 <= total_syllables <= 36:
                confidence += 0.20

            # Penalize very long metres in short verses
            if chandas == "वसन्ततिलका" and total_syllables < 30:
                confidence -= 0.15

        # ----------------------------
        # Finalize
        # ----------------------------
        adjusted.append(
            {
                "chandas": chandas,
                "confidence": round(max(confidence, 0.0), 3),
            }
        )

    # Sort by adjusted confidence
    adjusted.sort(key=lambda x: x["confidence"], reverse=True)
    return adjusted
