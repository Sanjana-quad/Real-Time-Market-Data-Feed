from kafka import KafkaProducer
import json
import time
import random

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def generate_stock_tick(symbol):
    return {
        'symbol': symbol,
        'price': round(random.uniform(100, 500), 2),
        'timestamp': time.time()
    }

if __name__ == '__main__':
    symbols = ['AAPL','GOOG','TSLA']
    while True:
        tick = generate_stock_tick(random.choice(symbols))
        producer.send('stock-ticks', tick)
        print(f"Sent: {tick}")
        time.sleep(1)  # 1 tick per second
