import builtins


def detect_delimiter(text_input, candidate_delimiters=[",", ";", "\t", "|"]) -> dict:
    """
    Detect the most likely delimiter in raw text input.

    Returns:
    {
        "status": "SUCCESS" | "FAILED",
        "result": {
            "delimiter": str | None
        },
        "metadata": {
            "confidence": float,
            "rows_analyzed": int,
            "candidate_scores": dict
        }
    }
    """

    import builtins

    # -----------------------------
    # 1. Normalize input
    # -----------------------------
    if isinstance(text_input, str):
        lines = [l.strip() for l in text_input.splitlines() if l.strip()]
    elif isinstance(text_input, (list, tuple, set)):
        lines = [str(l).strip() for l in text_input if str(l).strip()]
    else:
        return {
            "status": "FAILED",
            "result": {"delimiter": None},
            "metadata": {"confidence": 0.0, "rows_analyzed": 0, "candidate_scores": {}},
        }

    if not text_input:
        return {
            "status": "FAILED",
            "result": {"delimiter": None},
            "metadata": {"confidence": 0.0, "rows_analyzed": 0, "candidate_scores": {}},
        }

    # -----------------------------
    # 2. Scoring candidates
    # -----------------------------
    candidate_scores = {}
    best_delimiter = None
    best_score = -1

    for d in candidate_delimiters:
        column_counts = []

        for line in lines:
            column_counts.append(len(line.split(d)))

        if not column_counts:
            continue

        most_common = builtins.max(set(column_counts), key=column_counts.count)

        stability = column_counts.count(most_common)
        avg_cols = builtins.sum(column_counts) / len(column_counts)

        # penalize meaningless splits
        if avg_cols < 2:
            score = 0
        else:
            score = stability * avg_cols

        candidate_scores[d] = score

        if score > best_score:
            best_score = score
            best_delimiter = d

    # -----------------------------
    # 3. Confidence calculation
    # -----------------------------
    total_score = builtins.sum(candidate_scores.values())

    if total_score == 0:
        confidence = 0.0
    else:
        probabilities = {k: v / total_score for k, v in candidate_scores.items()}

    confidence = probabilities[best_delimiter]

    # -----------------------------
    # 4. Return standard format
    # -----------------------------
    return {
        "status": "SUCCESS" if best_delimiter else "FAILED",
        "result": {"delimiter": best_delimiter},
        "metadata": {
            "confidence": builtins.round(confidence, 4),
            "rows_analyzed": builtins.len(lines),
            "candidate_scores": candidate_scores,
        },
    }
