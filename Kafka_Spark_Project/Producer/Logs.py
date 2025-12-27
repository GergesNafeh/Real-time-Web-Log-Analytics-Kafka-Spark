from kafka import KafkaProducer
import time
import re

TOPIC_NAME = 'WEB-log'
KAFKA_SERVER = '172.16.113.131:9092'
LOG_FILE = '/home/bigdata/Kafka_Spark_Project/Data/access.log'

producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda v: v.encode('utf-8')
)

count = 0
current_log = []
ip_regex = re.compile(r'^\d+\.\d+\.\d+\.\d+')  

try:
    with open(LOG_FILE, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            if ip_regex.match(line) and current_log:
                full_log = " ".join(current_log)
                producer.send(TOPIC_NAME, value=full_log)
                producer.flush()
                count += 1
                print(f"Log #{count}: {full_log}\n")
                current_log = []
                time.sleep(1)

            current_log.append(line)


        if current_log:
            full_log = " ".join(current_log)
            producer.send(TOPIC_NAME, value=full_log)
            producer.flush()
            count += 1
            print(f"Log #{count}: {full_log}\n")

except KeyboardInterrupt:
    print("\n⚠️ Program stopped by user")
finally:
    producer.close()
    print(f"\n Total logs sent: {count}")
