from pyspark.sql.functions import col, lower, regexp_replace, trim
import pandas

def clean_text(df, column="experience"):
    """
    Cleans text columns for NLP processing.
    """

    if column not in df.columns:
        return {
            "status": "FAILED",
            "result": {"dataframe": None},
            "metadata": {"reason": "column not found"}
        }

    cleaned_df = df.withColumn(
        column,
            trim(
            lower(
                regexp_replace(col(column), r"[^a-zA-Z0-9 ]", "")
            )
            )
    )

    return {
        "status": "SUCCESS",
        "result": {
            "dataframe": cleaned_df
        },
        "metadata": {
            "transformed_column": column
        }
    }





