import pyspark
import pandas as pd
import numpy as np
import pyspark.sql.functions as F
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from src.processing.extract_skills import extract_skills
spark = SparkSession.builder.appName("find_overlap").getOrCreate()

from pyspark.sql import functions as F

def find_overlap(profile_skills, jobs_skills) -> dict:
    """
    Computes skill overlap between profile and job datasets.

    Assumption:
    - profile_df.skills is array<string>
    - jobs_df.skills is array<string>
    """

    # -----------------------------
    # 1. Validate input (Spark-safe)
    # -----------------------------
    if profile_skills is None or jobs_skills is None:
        return {
            "status": "FAILED",
            "message": "Input DataFrames are None",
            "overlap_count": 0,
            "overlap_skills": []
        }

    # -----------------------------
    # 2. Explode arrays into rows
    # -----------------------------
    profile_exploded = profile_skills.select(
        F.explode("skills").alias("skill")
    ).distinct()

    jobs_exploded = jobs_skills.select(
        F.explode("skills").alias("skill")
    ).distinct()

    # -----------------------------
    # 3. Inner join = intersection
    # -----------------------------
    overlap_df = profile_exploded.join(
        jobs_exploded,
        on="skill",
        how="inner"
    ).distinct()

    # -----------------------------
    # 4. Collect results
    # -----------------------------
    overlap_list = [row["skill"] for row in overlap_df.collect()]
    overlap_count = len(overlap_list)
    

    # -----------------------------
    # 5. Return structured output
    # -----------------------------
    return {
        "status": "SUCCESS",
        "overlap_count": overlap_count,
        "overlap_skills": overlap_list,
        "result_df": overlap_df
    }
    