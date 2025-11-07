# 🧩 Real-Time Market Data Feed Pipeline – Milestone 1

### 🎯 Goal
Simulate stock-market tick data and stream it through Apache Kafka to understand core producer-consumer workflows.

---

## 📁 Project Structure
realtime-market-data-pipeline/
-docker-compose.yml
-producer/
--producer.py
--__init__.py
-consumer/
-- consumer.py
--__init__.py
-logs/
--analytics.log
-analytics/
--moving_average.py
--alerts.py
--__init__.py
-README.md


---

## ⚙️ Tech Stack
- **Language:** Python 3.x  
- **Messaging System:** Apache Kafka (on Docker)  
- **Dependencies:** `kafka-python`, `pandas`, `matplotlib`

---

## 🚀 Setup & Run
1. **Start Kafka Cluster**
   ```bash
   docker-compose up -d

2. **Create Topic**
    ```bash
    docker exec -it <kafka_container_id> bash
    kafka-topics --bootstrap-server localhost:9092 --create --topic stock-ticks --partitions 3 --replication-factor 1

3. **Run Producer**
    ```bash 
    python producer/producer.py

4. **Run Consumer**
    ```bash
    python consumer/consumer.py

### Output example
    ```bash
    Sent: {'symbol': 'AAPL', 'price': 215.67, 'timestamp': 1730896201.0}
    Received: {'symbol': 'AAPL', 'price': 215.67, 'timestamp': 1730896201.0}

---

## 🧠 What I Learned

Installed Kafka with Docker Compose

Created topics and connected producers & consumers

Understood message serialization and partitioning

---

# 🧮 Milestone 2 – Real-Time Analytics

### 🎯 Goal
Enhance the consumer to compute moving averages and trigger alerts for sudden price changes.

---

## ⚙️ How It Works
1. **Moving Average (MA)** – Rolling window of last 5 prices per symbol.
2. **Alert System** – Triggers alert if price change ≥ 3%.
3. **Logging** – All analytics saved in `logs/analytics.log`.

---

## 🧠 What I Learned
- Implemented in-memory rolling computations using `deque` & `pandas`.
- Designed modular consumer architecture (analytics separated from core logic).
- Introduced structured logging for analytics events.


# Milestone 3 – Analytics Layer (Moving Average + Alerts)

### 🎯 Objective
Enhance the consumer to perform live stock analytics — calculating moving averages and detecting large price swings in real time.

---

## 🧩 Components

### 1. Moving Average Calculator
File: `analytics/moving_average.py`

### 2. Price Alert System
File: `analytics/alerts.py`

## ⚙️ How It Works

>consumer.py fetches stock ticks from Kafka.

>For each tick:
>>Updates the moving average for that symbol.
>>Checks for price swings beyond a threshold.
>>Logs analytics in logs/analytics.log.

## 🧠 Example Output
    ```bash
    AAPL | Price: 314.66 | MA(5): 312.12
    ⚠️ AAPL changed by 3.45%
    GOOG | Price: 201.52 | MA(5): 205.67