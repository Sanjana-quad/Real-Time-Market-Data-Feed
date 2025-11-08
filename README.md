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

1. **consumer.py fetches stock ticks from Kafka.**

2. **For each tick:**
    - Updates the moving average for that symbol.
    - Checks for price swings beyond a threshold.
    - Logs analytics in `logs/analytics.log`.

## 🧠 Example Output
    ```bash
    AAPL | Price: 314.66 | MA(5): 312.12
    ⚠️ AAPL changed by 3.45%
    GOOG | Price: 201.52 | MA(5): 205.67

# Milestone 4 – Real-Time Analytics API

### 🎯 Objective
Expose live analytics via a REST API for visualization dashboards.

---

## ⚙️ Components
| Component | Description |
|------------|--------------|
| `api/app.py` | Flask REST API serving analytics |
| `consumer/consumer.py` | Posts analytics updates to the API |
| `producer/producer.py` | Continues producing stock ticks to Kafka |

---

## 🧠 Endpoints
| Method | Endpoint | Description |
|---------|-----------|-------------|
| GET | `/data` | Get analytics for all stocks |
| GET | `/data/<symbol>` | Get analytics for one stock |
| POST | `/update` | Update data (used internally by consumer) |

---

## 🔗 Example Response
```json
[
  {
    "symbol": "AAPL",
    "price": 312.45,
    "moving_average": 310.78,
    "alert": "⚠️ AAPL changed by 3.10%",
    "timestamp": 1730871025.145
  }
]

## 🖥️ Milestone 5: Real-Time Dashboard Integration

### 🎯 Objective
Build a live-updating dashboard to visualize stock prices and moving averages coming through Kafka → Consumer → SQLite → Flask.

---

### 🧰 Tools & Technologies
- **Flask** — Serves the dashboard and API endpoints  
- **Chart.js** — Frontend charting library for real-time line charts  
- **SQLite (via database.py)** — Lightweight persistence layer  
- **Fetch API (JavaScript)** — Periodically fetches new data from `/data` endpoint  
- **Matplotlib (optional)** — For offline plotting in `plot_live.py`

---

### 📂 Project Structure Additions
realtime-market-data-pipeline/
-api/
--templates/
--- dashboard.html # Real-time Chart.js dashboard
-- app.py # Flask backend serving API + dashboard
--database.py # SQLite + async writer
- analytics/
-- plot_live.py


---

### ⚙️ How It Works
1. **Producer** sends stock ticks (`symbol`, `price`, `timestamp`) to Kafka topic `stock-ticks`.  
2. **Consumer** reads ticks → computes 5-point moving average → pushes to SQLite (via async writer).  
3. **Flask app** exposes APIs:
   - `/data` → latest cached analytics  
   - `/data/<symbol>` → symbol history from SQLite  
   - `/dashboard` → interactive Chart.js page that auto-refreshes data  
4. **Dashboard** polls `/data` every 2 seconds and dynamically updates line charts.

---

### 🧠 What You’ll Learn
| Concept | Learning Outcome |
|----------|------------------|
| Flask Integration | How to serve REST + frontend from one backend |
| Chart.js | Building simple real-time web visualizations |
| REST Polling | How clients continuously fetch and visualize streaming data |
| Data Flow | Kafka → Consumer → DB → Flask → Dashboard |

---

### 🚀 Run Instructions
1. Start Kafka services  
   ```bash
   docker-compose up -d

2. Run the producer
    ```bash
    python producer.py

3. Run the consumer
    ```bash
    python consumer.py

4. Start Flask app
    ```bash
    python app.py

5. Open browser → `http://localhost:5000/dashboard`

---

## 🧩 Next Steps (optional ideas)

1. Add color-coded alerts (price spikes in red)

2. Deploy dashboard using Render or Railway

3. Convert to WebSocket-based live streaming instead of polling