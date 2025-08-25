from pyspark.sql import SparkSession
from pyspark.sql.functions import col, date_trunc, sum as _sum, countDistinct

def main():
    spark = (SparkSession.builder.appName("RetailDemand360-BatchETL").getOrCreate())
    bronze = spark.read.parquet("./lake/bronze/transactions")
    silver = bronze.dropna(subset=["store_id","product_id","amount"]).filter(col("amount")>0)
    silver.write.mode("overwrite").parquet("./lake/silver/transactions")
    by_day = (silver.groupBy(date_trunc("day","ts").alias("day"), "store_id","product_id")
              .agg(_sum("qty").alias("units"), _sum("amount").alias("revenue")))
    by_day.write.mode("overwrite").parquet("./lake/gold/daily_store_product")
    kpis = (silver.groupBy(date_trunc("day","ts").alias("day"))
            .agg(_sum("amount").alias("daily_revenue"),
                 countDistinct("store_id").alias("active_stores"),
                 countDistinct("product_id").alias("active_products")))
    kpis.write.mode("overwrite").parquet("./lake/gold/daily_kpis")

if __name__ == "__main__":
    main()
