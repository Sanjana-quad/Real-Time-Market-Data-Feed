# 🧩 Real-Time Market Data Feed Pipeline – Milestone 1

### 🎯 Goal
Simulate stock-market tick data and stream it through Apache Kafka to understand core producer-consumer workflows.

---

## 📁 Project Structure
realtime-market-data-pipeline/
-docker-compose.yml
-producer/
--producer.py
-consumer/
-- consumer.py
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

