from src.ingestion.parse_file import parse_file
from src.ingestion.detect_delimiter import detect_delimiter
from src.ingestion.detect_header import detect_header 
from pyspark.sql.types import *
from pyspark.sql import SparkSession
import pandas as pd

spark = SparkSession.builder.appName("Spark DataFrames").getOrCreate()


def create_dataframe(records, spark, schema=None):
    """
    Converts structured records into Spark DataFrame (Silver layer).
    PURE FUNCTION: no parsing, no detection.
    """

    # 1. Validate input
    if not records or len(records) == 0:
        return {
            "status": "FAILED",
            "result": {"dataframe": None},
            "metadata": {
                "row_count": 0,
                "columns": []
            }
        }

    # 2. Create Spark DataFrame
    df = spark.createDataFrame(records, schema=schema)

    # 3. Metadata
    return {
        "status": "SUCCESS",
        "result": {
            "dataframe": df
        },
        "metadata": {
            "row_count": df.count(),
            "columns": df.columns
        }
    }


