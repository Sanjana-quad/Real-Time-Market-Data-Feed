from flask import Flask, jsonify, request
from threading import Lock

app = Flask(__name__)

# Shared data structure
analytics_data = {}
lock = Lock()

@app.route('/')
def home():
    return """
    <h2>Real-Time Market Data API</h2>
    <p>Available endpoints:</p>
    <ul>
        <li>GET /data — all stock analytics</li>
        <li>GET /data/&lt;symbol&gt; — specific stock data</li>
        <li>POST /update — push analytics update</li>
    </ul>
    """


@app.route('/update', methods=['POST'])
def update_data():
    """Receive analytics updates from consumer"""
    new_data = request.get_json()
    symbol = new_data.get('symbol')
    if not symbol:
        return {"error": "symbol missing"}, 400

    with lock:
        analytics_data[symbol] = new_data
    return {"status": "updated"}, 200


@app.route('/data', methods=['GET'])
def get_all_data():
    """Get all stock analytics"""
    with lock:
        return jsonify(list(analytics_data.values()))


@app.route('/data/<symbol>', methods=['GET'])
def get_symbol_data(symbol):
    """Get one symbol's analytics"""
    with lock:
        data = analytics_data.get(symbol.upper())
    if not data:
        return {"error": "symbol not found"}, 404
    return jsonify(data)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
