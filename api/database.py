import sqlite3
import threading
import queue
import time
import os
from contextlib import closing

# --- Configuration ---
# DB_FILE = "analytics_data.db"

DB_FILE = os.path.join(os.path.dirname(__file__), "..", "analytics_data.db")
DB_FILE = os.path.abspath(DB_FILE)     # ensures both Flask & Consumer share same DB path
BATCH_SIZE = 50          # Flush to DB after these many records
FLUSH_INTERVAL = 2       # Seconds between flush attempts

# --- Global Components ---
lock = threading.Lock()
insert_queue = queue.Queue()
cache = {}  # {symbol: {price, moving_average, alert, timestamp}}

stop_event = threading.Event()


# --- Helper: SQLite Connection ---
def _get_connection():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


# --- Initialization ---
def init_db():
    """Create DB file + analytics table if missing."""
    os.makedirs(os.path.dirname(DB_FILE) or ".", exist_ok=True)
    with lock, closing(_get_connection()) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                price REAL,
                moving_average REAL,
                alert TEXT,
                timestamp REAL
            )
        """)
        conn.commit()


# --- Insertion (Thread-Safe) ---
def insert_record(symbol, price, moving_average, alert, timestamp):
    """Queue a new analytics record for async batch insertion."""
    if not symbol:
        return

    symbol = symbol.upper()

    # Update in-memory cache
    cache[symbol] = {
        "symbol": symbol,
        "price": price,
        "moving_average": moving_average,
        "alert": alert,
        "timestamp": timestamp,
    }

    # Add to write queue
    insert_queue.put((symbol, price, moving_average, alert, timestamp))
    _insert_counter += 1
    if _insert_counter % 10 == 0:
        print(f"[DB] insert_record called {_insert_counter} times; queue size={insert_queue.qsize()}")

# --- Background Batch Writer ---
def _flush_to_db():
    """Flush queued records to SQLite in batches."""
    while not stop_event.is_set():
        batch = []
        try:
            # Collect up to BATCH_SIZE or wait for FLUSH_INTERVAL
            while len(batch) < BATCH_SIZE:
                record = insert_queue.get(timeout=FLUSH_INTERVAL)
                batch.append(record)
        except queue.Empty:
            pass  # time-based flush trigger

        if batch:
            with lock, closing(_get_connection()) as conn:
                try:
                    conn.executemany("""
                        INSERT INTO analytics (symbol, price, moving_average, alert, timestamp)
                        VALUES (?, ?, ?, ?, ?)
                    """, batch)
                    conn.commit()
                    print(f"[DB] Flushed {len(batch)} records to DB (file: {DB_FILE})")
                except Exception as e:
                    print(f"[DB ERROR] Failed batch insert: {e}")


# --- Thread Controls ---
def start_background_writer():
    """Start the async background DB writer thread."""
    t = threading.Thread(target=_flush_to_db, daemon=True)
    t.start()
    # print("[DB] Background writer started.")
    print(f"[DB] Background writer started. Using: {DB_FILE}")


def stop_background_writer():
    """Gracefully stop the background writer thread."""
    stop_event.set()
    time.sleep(FLUSH_INTERVAL + 1)  # wait for flush
    print("[DB] Background writer stopped.")


# --- Retrieval Functions ---
def get_latest_records():
    # """Return latest records directly from in-memory cache (fast)."""
    # return list(cache.values())
    """Return the most recent record per symbol by querying the DB file."""
    # with closing(sqlite3.connect(DB_FILE)) as conn:
    with lock, closing(_get_connection()) as conn:
        # conn.row_factory = sqlite3.Row
        cursor = conn.execute("""
            SELECT a.symbol, a.price, a.moving_average, a.alert, a.timestamp
            FROM analytics a
            INNER JOIN (
                SELECT symbol, MAX(timestamp) AS max_time
                FROM analytics
                GROUP BY symbol
            ) latest
            ON a.symbol = latest.symbol AND a.timestamp = latest.max_time
            ORDER BY a.symbol
        """)
        rows = cursor.fetchall()
        return [dict(r) for r in rows]


def get_symbol_history(symbol, limit=50):
    """Return last N records for a given symbol from SQLite."""
    with lock, closing(_get_connection()) as conn:
        cursor = conn.execute("""
            SELECT symbol, price, moving_average, alert, timestamp
            FROM analytics
            WHERE symbol = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (symbol.upper(), limit))
        return [dict(row) for row in cursor.fetchall()]
