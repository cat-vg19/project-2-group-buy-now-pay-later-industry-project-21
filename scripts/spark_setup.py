"""
spark_setup.py

Shared SparkSession builder.
"""

from pyspark.sql import SparkSession

# PySpark 3.5.x needs `distutils` (removed from stdlib in Python 3.12+);
# PySpark 4.0+ doesn't. See README if this raises on your setup.
try:
    import distutils  # noqa: F401
except ModuleNotFoundError:
    import pyspark
    if int(pyspark.__version__.split(".")[0]) < 4:
        raise ModuleNotFoundError(
            "distutils is required for PySpark 3.5.x on Python 3.12+. Run: "
            "pip install standard-distutils"
        )


def get_spark(app_name: str = "bnpl-industry-project",
               driver_memory: str = "6g",
               shuffle_partitions: int = 8) -> SparkSession:
    """
    local[*] SparkSession. shuffle_partitions defaults low (8, vs
    Spark's 200 default) -- this project's data volume doesn't need more.
    """
    return (
        SparkSession.builder
        .appName(app_name)
        .master("local[*]")
        .config("spark.sql.repl.eagerEval.enabled", True)
        .config("spark.driver.memory", driver_memory)
        .config("spark.sql.shuffle.partitions", str(shuffle_partitions))
        .getOrCreate()
    )