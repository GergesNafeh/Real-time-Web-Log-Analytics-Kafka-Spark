# Real-time Web Logs Analytics with Kafka, Spark Streaming & HBase

## Description
This project implements a **real-time web log analytics pipeline** using Kafka, Spark Structured Streaming, and HBase.  
It ingests web server logs, parses them, performs analytics such as counting HTTP status codes and tracking top IP addresses, and stores the processed data in HBase for further querying.  

This pipeline demonstrates a **full end-to-end streaming data workflow** from ingestion to storage and analysis.


---

                                     ┌───────────────────┐
                                     │  Web Server Logs  │
                                     └──────────┬────────┘
                                                │
                                                ▼
                                     ┌───────────────────┐
                                     │    Kafka Topic    │
                                     └──────────┬────────┘
                                                │
                                                ▼
                           ┌───────────────────────────────────────┐
                           │     Spark Structured Streaming        │
                           │   - Parsing Logs                      │
                           │   - Aggregation (Status Count)        │
                           │   - Top IPs Detection                 │
                           │   - Write to HBase                    │
                           └──────────────────┬────────────────────┘
                                              │
                                              ▼
                                     ┌───────────────────┐
                                     │       HBase       │
                                     │  (WEB-logs Table) │
                                     └───────────────────┘



---

## 📝 Project Overview

This project is a real-time **Web Log Streaming & Analysis Pipeline** built using:

- **Kafka** → As a real-time messaging system to stream incoming logs  
- **Spark Structured Streaming** → To parse, clean, and analyze logs continuously  
- **HBase** → For scalable NoSQL storage of processed data  
- **Linux VM** → For runtime environment and services deployment  

📌 The system processes unstructured Apache Web Server logs and extracts:

| Data Extracted | Example |
|--------------|---------|
| Client IP | `54.36.149.41` |
| Timestamp | `22/Jan/2019:03:56:14 +0330` |
| HTTP Method | `GET / POST` |
| URL | `/login` |
| Response Status Code | `200 / 404 / 500` |
| Response Size | `30577 bytes` |

🎯 **Main Objectives**
- Track **traffic trends** in real-time
- Monitor **top requested IPs**
- Measure **server performance**
- Store logs in **HBase** for scalable analytics & reporting

📊 The dashboard-like CLI output enables fast debugging & insights.

---

## Tools & Technologies
- **Kafka**: Message broker for streaming web logs
- **Apache Spark Structured Streaming**: Real-time data processing
- **HBase**: NoSQL database for storing processed logs
- **Python**: Programming language
- **HappyBase**: Python library for HBase integration
- **Linux (CentOS)**: Development and execution environment

---

## Features
- Real-time ingestion of web logs via Kafka
- Log parsing to extract IP, timestamp, method, URL, status, and size
- Analytics:
  - Count of HTTP status codes
  - Top requesting IP addresses
- Storing processed logs into HBase (table: `WEB-logs`, column family: `LOGs`)
- Console output for monitoring
- Checkpointing for fault tolerance

---

## ⚠️ Challenges Faced & Solutions

| Issue / Challenge | Description | Solution |
|------------------|-------------|----------|
| Kafka connection not established | Spark wasn't able to read Kafka topic | Corrected server IP + allowed VM network access |
| Data not parsed correctly | Log pattern mismatch caused blank fields | Updated regex extractions to match full log format |
| Duplicate data in streaming output | Spark was reprocessing the same batch | Configured checkpoint + `startingOffsets="latest"` |
| HBase write errors | Missing column family config | Defined column family `LOGs` in creation |
| Spark performance warnings | High delay in streaming processing | Reduced batch size & optimized console sink |
| Kafka Producer stopped sending logs | Log file path wrong in VM | Set absolute correct file path and verified permissions |
| Display formatting issues in console | Messy output for status and IP analytics | Used pretty console tables & grouping |

---

## 📌 Key Learnings

✔ Hands-on experience with **real-time data engineering**  
✔ Understanding how streaming lifecycle works (Producer → Consumer → Storage)  
✔ Improved debugging skills using logs from Spark & Kafka  
✔ Working with NoSQL storage for analytical data  
✔ Data parsing using regex expressions  
✔ End-to-end pipeline architecture & deployment inside VM  

---

## 🔮 Future Improvements

- Create **Power BI / Tableau Dashboard** connected to HBase
- Add **GeoIP lookup** to analyze geographic access patterns
- Implement **alerts** for suspicious IP activities (security use-case)
- Expand pipeline to **multi-topic Kafka producers**
- Push structured data into **Hive** for batch analytics

---


---

## 📷 Screenshots

### 🔹 1️⃣ Log File Sample
> Sample of the raw logs before processing  
<img width="1366" height="768" alt="Log File" src="https://github.com/user-attachments/assets/566f4c98-05b7-4102-b72c-09b13b81eb7f" />



---

### 🔹 2️⃣ Kafka Producer View
> Logs being streamed in real-time to Kafka  
<img width="1287" height="456" alt="ProducerLog" src="https://github.com/user-attachments/assets/2977bb47-f442-4682-bdbc-3a3f34f3250b" />


---

### 🔹 3️⃣ Spark Streaming Logs (Raw)
> Spark consumer receives logs raw before analysis  

<img width="1286" height="443" alt="SparkLogs" src="https://github.com/user-attachments/assets/e1b1b9fe-4967-484c-a815-265fc2e65b54" />

---

### 🔹 4️⃣ Spark Analysis Output
> Real-time aggregated analysis (status codes & top IPs)  
<img width="541" height="391" alt="Analysis" src="https://github.com/user-attachments/assets/f8d97ed2-e4d7-429d-8376-bd259106f984" />


---




---

## Installation & Setup

1. **Install Kafka, HBase, Spark, Python, HappyBase**
2. **Start HBase**
  ## How to Run & Sample Output

## 🚀 Running the Real-Time Web Log Analytics Pipeline

```bash
# 1️⃣ Start HBase service
start-hbase.sh

# Create table for storing processed logs
hbase shell
create 'WEB-logs', 'LOGs'
exit

# 2️⃣ Start Kafka Broker
kafka-server-start.sh config/server.properties

# 3️⃣ Run Spark Streaming Consumer (parsing + analytics + write to HBase)
spark-submit spark_hbase_stream.py

# 4️⃣ Run Kafka Producer (send logs to topic)
python producer.py

# 5️⃣ Verify records stored in HBase
hbase shell
scan 'WEB-logs'

# Simple Output
 
54.36.149.41 - - [22/Jan/2019:03:56:14 +0330] "GET /filter/... HTTP/1.1" 200 30577
192.168.1.5 - - [22/Jan/2019:03:57:10 +0330] "POST /login HTTP/1.1" 404 512
...

#  Simple Analysis

+------+-----+
|status|count|
+------+-----+
|200   |150  |
|404   |10   |
|500   |2    |
+------+-----+
