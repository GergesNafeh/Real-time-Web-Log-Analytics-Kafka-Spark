from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_extract


spark = SparkSession.builder \
    .appName("KafkaWebLogs") \
    .getOrCreate()


spark.sparkContext.setLogLevel("WARN")


df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "172.16.113.131:9092") \
    .option("subscribe", "WEB-log") \
    .option("startingOffsets", "latest") \
    .load()


logs = df.selectExpr("CAST(value AS STRING) as log")


logs.printSchema()

# Parsing the log
parsed = logs.select(
    regexp_extract("log", r'^(\S+)', 1).alias("ip"),
    regexp_extract("log", r'\[(.*?)\]', 1).alias("timestamp"),
    regexp_extract("log", r'"(GET|POST|PUT|DELETE)', 1).alias("method"),
    regexp_extract("log", r'"(?:GET|POST|PUT|DELETE) (.*?) HTTP', 1).alias("url"),
    regexp_extract("log", r'" (\d{3}) ', 1).alias("status"),
    regexp_extract("log", r'" \d{3} (\d+)', 1).alias("size")
)


query = parsed.writeStream \
    .format("console") \
    .option("truncate", False) \
    .option("checkpointLocation", "/tmp/spark_checkpoint_web_logs") \
    .start()


query.awaitTermination()
