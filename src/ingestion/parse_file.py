import builtins
from src.ingestion.detect_delimiter import detect_delimiter
from src.ingestion.detect_header import detect_header


def parse_file(lines, delimiter, header_result):
    """
    Converts raw ingested text into structured records (Silver layer).
    """

    # -----------------------------
    # 1. Normalize input
    # -----------------------------
    cleaned = [l.strip() for l in lines if l and l.strip()]

    if not cleaned:
        return {
            "status": "FAILED",
            "result": {"data": []},
            "metadata": {
                "rows_parsed": 0,
                "rows_skipped": 0,
                "columns": []
            }
        }

    # -----------------------------
    # 2. Extract header info
    # -----------------------------
    header_index = header_result["result"]["header_row_index"]
    header_columns = header_result["result"]["header_columns"]

    # -----------------------------
    # 3. Build structured dataset
    # -----------------------------
    data = []
    skipped_rows = 0

    for i, row in enumerate(cleaned):

        # skip metadata + header
        if i <= header_index:
            continue

        values = row.split(delimiter['result']['delimiter'])

        # strict schema alignment check
        if len(values) != len(header_columns):
            skipped_rows += 1
            continue

        # clean values (basic hygiene step)
        values = [v.strip() for v in values]

        record = dict(zip(header_columns, values))
        data.append(record)

    # -----------------------------
    # 4. Return structured output
    # -----------------------------
    return {
        "status": "SUCCESS",
        "result": {
            "data": data
        },
        "metadata": {
            "rows_parsed": len(data),
            "rows_skipped": skipped_rows,
            "columns": header_columns
        }
    }

