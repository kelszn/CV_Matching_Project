import builtins
from src.ingestion.detect_delimiter import detect_delimiter

def detect_header(lines, delimiter)-> dict:
    """
    Detects header row in messy raw data using structural + semantic signals.
    """

    # -----------------------------
    # 1. Normalize input
    # -----------------------------
    cleaned = [l.strip() for l in lines if l and l.strip()]

    if not cleaned:
        return {
            "status": "FAILED",
            "result": {"header_row_index": None, "header_columns": []},
            "metadata": {"confidence": 0.0, "rows_scored": 0}
        }

    # -----------------------------
    # 2. Define header keywords (important heuristic)
    # -----------------------------
    header_keywords = {
        "id", "name", "experience", "profile", "job", "title",
        "description", "date", "email", "phone"
    }

    scores = []

    # -----------------------------
    # 3. Score each row
    # -----------------------------
    for i, line in enumerate(cleaned):
        parts = line.split(delimiter)
        col_count = len(parts)

        # --- Feature 1: text richness (not numeric-heavy)
        text_ratio = builtins.sum(
            any(c.isalpha() for c in p) for p in parts
        ) / builtins.max(col_count, 1)

        # --- Feature 2: structure consistency with next row
        if i + 1 < len(cleaned):
            next_parts = cleaned[i + 1].split(delimiter)
            structure_match = 1 if len(next_parts) == col_count else 0
        else:
            structure_match = 0

        # --- Feature 3: keyword presence bonus
        keyword_bonus = builtins.sum(
            1 for p in parts
            if p.lower().strip() in header_keywords
        ) / builtins.max(col_count, 1)

        # --- Final score (weighted)
        score = (
            (text_ratio * 0.5) +
            (structure_match * 0.3) +
            (keyword_bonus * 0.2)
        )

        scores.append(score)

    # -----------------------------
    # 4. Select best header candidate
    # -----------------------------
    best_index = builtins.max(range(len(scores)), key=lambda i: scores[i])
    best_score = scores[best_index]

    header_columns = cleaned[best_index].split(delimiter)

    # -----------------------------
    # 5. Return structured output
    # -----------------------------
    return {
        "status": "SUCCESS",
        "result": {
            "header_row_index": best_index,
            "header_columns": header_columns
        },
        "metadata": {
            "confidence": builtins.round(best_score, 4),
            "rows_scored": len(scores)
        }
    }







