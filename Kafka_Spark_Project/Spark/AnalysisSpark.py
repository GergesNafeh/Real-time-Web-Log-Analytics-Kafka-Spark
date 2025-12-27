from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_extract, to_timestamp, col

# -------------------------------
# Spark Session
# -------------------------------
spark = SparkSession.builder \
    .appName("KafkaWebLogsStreamingAnalysis") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# -------------------------------

# -------------------------------
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "172.16.113.131:9092") \
    .option("subscribe", "WEB-log") \
    .option("startingOffsets", "latest") \
    .load()

logs = df.selectExpr("CAST(value AS STRING) as log")

logs.printSchema()

# -------------------------------
# Parsing the log
# -------------------------------
parsed = logs.select(
    regexp_extract("log", r'^(\S+)', 1).alias("ip"),
    regexp_extract("log", r'\[(.*?)\]', 1).alias("timestamp"),
    regexp_extract("log", r'"(GET|POST|PUT|DELETE)', 1).alias("method"),
    regexp_extract("log", r'"(?:GET|POST|PUT|DELETE) (.*?) HTTP', 1).alias("url"),
    regexp_extract("log", r'" (\d{3}) ', 1).alias("status"),
    regexp_extract("log", r'" \d{3} (\d+)', 1).alias("size")
)


parsed_ts = parsed.withColumn("ts", to_timestamp("timestamp", "dd/MMM/yyyy:HH:mm:ss Z"))

# -------------------------------
# Analysis with Watermark
# -------------------------------
base_path = "/home/bigdata/Desktop/output"

# 4.1 Count requests per status code
status_count = parsed_ts.withWatermark("ts", "1 minute") \
    .groupBy("status") \
    .count()

# 4.2 Errors فقط (>=400)
errors_df = parsed_ts.withWatermark("ts", "1 minute") \
    .filter(col("status").cast("int") >= 400)

# 4.3 Top IPs
top_ips = parsed_ts.withWatermark("ts", "1 minute") \
    .groupBy("ip") \
    .count() \
    .orderBy("count", ascending=False)

# -------------------------------
# Write Streams ( Console)
# -------------------------------
# Top IPs → Console
query_top_ips = top_ips.writeStream \
    .outputMode("complete") \
    .format("console") \
    .option("truncate", False) \
    .option("checkpointLocation", f"{base_path}/checkpoint/top_ips_console") \
    .start()

# -------------------------------
# Keep Streaming
# -------------------------------
spark.streams.awaitAnyTermination()
