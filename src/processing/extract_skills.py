from pyspark.sql.functions import col, udf
from pyspark.sql.types import ArrayType, StringType

SKILL_KEYWORDS = {
    "spark", "etl", "airflow", "sql", "python",
    "pandas", "databricks", "ml", "machinelearning",
    "dashboard", "powerbi"
}


def extract_skills(df, column="experience"):
    """
    Extracts skills from text using rule-based matching.
    """

    if column not in df.columns:
        return {
            "status": "FAILED",
            "result": {"dataframe": None},
            "metadata": {"reason": "column not found"}
        }

    def skill_extractor(text):
        if not text:
            return []
        words = text.split()
        return list(set([w for w in words if w in SKILL_KEYWORDS]))

    extract_udf = udf(skill_extractor, ArrayType(StringType()))

    new_df = df.withColumn("skills", extract_udf(col(column)))

    return {
        "status": "SUCCESS",
        "result": {"dataframe": new_df},
        "metadata": {"new_column": "skills"}
    }