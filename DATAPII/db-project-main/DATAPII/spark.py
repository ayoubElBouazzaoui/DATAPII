
from pyspark.sql import SparkSession
import findspark

# Initialize Spark using findspark
findspark.init("spark-3.3.1-bin-hadoop3")

# Create a Spark session
spark = SparkSession.builder \
    .master("local") \
    .appName("Linear Regression Model") \
    .config("spark.executor.memory", "1gb") \
    .getOrCreate()

# Create a Spark context
sc = spark.sparkContext

