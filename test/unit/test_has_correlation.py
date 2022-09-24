from typing import Collection
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from cuallee import Check, CheckLevel
from operator import attrgetter as at
from toolz import compose
import numpy as np
import pandas as pd
from loguru import logger


def test_positive_correlation(spark: SparkSession):
    check = Check(CheckLevel.WARNING, "PyTestCheck")
    df = spark.range(10).withColumn("id2", F.col("id") * 10)
    logger.info(df.collect())
    check.has_correlation("id", "id2", 1.0)
    logger.info(check)
    assert check.validate(spark, df).first().status == "PASS"


def test_no_correlation(spark: SparkSession):
    check = Check(CheckLevel.WARNING, "PyTestCheck")
    df = spark.createDataFrame(
        pd.DataFrame({"id": np.arange(10), "id2": np.random.randn(10)})
    )
    check.has_correlation("id", "id2", 1.0)
    assert check.validate(spark, df).first().status == "FAIL"


def test_correlation_value(spark: SparkSession):
    check = Check(CheckLevel.WARNING, "PyTestCheck")
    df = spark.range(10).withColumn("id2", F.col("id") * 10)
    check.has_correlation("id", "id2", 1.0)
    assert str(check.validate(spark, df).first().value) == "1.0"