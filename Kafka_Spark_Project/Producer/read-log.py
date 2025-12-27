with open("/home/bigdata/Kafka_Spark_Project/Data/access.log","r") as file:
     for line in file:
          print(line.strip())
