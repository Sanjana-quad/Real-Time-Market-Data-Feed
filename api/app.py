from flask import Flask, jsonify, request
from threading import Lock
from database import init_db, insert_record, get_latest_records, get_symbol_history, start_background_writer, stop_background_writer
import atexit

app = Flask(__name__)

# 1️⃣ Initialize database
init_db()
start_background_writer()

# # 2️⃣ Shared in-memory cache
# analytics_data = {}
# lock = Lock()

# # 3️⃣ On startup: preload latest records into memory
# latest_records = get_latest_records()
# for rec in latest_records:
#     analytics_data[rec["symbol"]] = rec


@app.route('/')
def home():
    return """
    <h2>Real-Time Market Data API</h2>
    <p>Available endpoints:</p>
    <ul>
        <li>GET /data — all stock analytics (cached in-memory)</li>
        <li>GET /data/&lt;symbol&gt; — specific stock history (from SQLite)</li>
        <li>POST /update — push analytics update (writes to both)</li>
    </ul>
    """


@app.route('/update', methods=['POST'])
def update_data():
    """Receive analytics updates from consumer"""
    new_data = request.get_json(force=True)
    symbol = new_data.get('symbol')
    if not symbol:
        return {"error": "symbol missing"}, 400

    # with lock:
    #     # 1️⃣ Update in-memory cache
    #     analytics_data[symbol] = new_data

    #     # 2️⃣ Persist in SQLite
    #     insert_record(
    #         symbol=symbol,
    #         price=new_data.get('price'),
    #         moving_average=new_data.get('moving_average'),
    #         alert=new_data.get('alert'),
    #         timestamp=new_data.get('timestamp')
    #     )
    # return {"status": "updated and stored"}, 200

    try:
        insert_kwargs = {
            "symbol": symbol,
            "price": new_data.get('price'),
            "moving_average": new_data.get('moving_average'),
            "alert": new_data.get('alert'),
            "timestamp": new_data.get('timestamp')
        }
        # Import here to avoid circular import if consumer imports app
        from database import insert_record
        insert_record(**insert_kwargs)
        return {"status": "queued"}, 200
    except Exception as e:
        return {"error": str(e)}, 500


@app.route('/data', methods=['GET'])
def get_all_data():
    """Return all latest analytics from in-memory cache"""
    # with lock:
    #     return jsonify(list(analytics_data.values()))
    data = get_latest_records()  # returns list of dicts (cache)
    return jsonify(data)

@app.route('/data/<symbol>', methods=['GET'])
def get_symbol_data(symbol):
    """Return history for a specific stock (from DB)"""
    data = get_symbol_history(symbol.upper())
    if not data:
        return {"error": "symbol not found"}, 404
    return jsonify(data)


# Graceful shutdown hook to stop the background writer
@atexit.register
def shutdown():
    try:
        stop_background_writer()
    except Exception:
        pass

if __name__ == '__main__':
    app.run(port=5000, debug=True)
