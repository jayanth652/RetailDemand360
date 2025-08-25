from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType

SCHEMA = StructType([
    StructField("event_id", StringType()),
    StructField("ts", StringType()),
    StructField("store_id", StringType()),
    StructField("product_id", StringType()),
    StructField("category", StringType()),
    StructField("unit_price", DoubleType()),
    StructField("qty", IntegerType()),
    StructField("amount", DoubleType()),
    StructField("promotion", IntegerType()),
])

def main():
    spark = (SparkSession.builder.appName("RetailDemand360-Streaming").getOrCreate())
    df = (spark.readStream.format("cloudFiles").option("cloudFiles.format", "json").schema(SCHEMA).load("data/generator"))
    bronze = (df.withColumn("ts", to_timestamp(col("ts"))))
    q = (bronze.writeStream.format("parquet").option("checkpointLocation","./.chk/bronze").option("path","./lake/bronze/transactions").outputMode("append").start())
    q.awaitTermination()

if __name__ == "__main__":
    main()
