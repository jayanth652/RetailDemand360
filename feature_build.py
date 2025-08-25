from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg

def main():
    spark = (SparkSession.builder.appName("RetailDemand360-FeatureStore").getOrCreate())
    daily = spark.read.parquet("./lake/gold/daily_store_product")
    w7 = (daily.groupBy("store_id","product_id").agg(avg("units").alias("avg_units_alltime")))
    latest = daily.selectExpr("max(day) as day").collect()[0]["day"]
    snapshot = daily.filter(col("day")==latest).join(w7, ["store_id","product_id"], "left")
    snapshot.write.mode("overwrite").parquet("./features/snapshot")
    print("Wrote features to ./features/snapshot")

if __name__ == "__main__":
    main()
