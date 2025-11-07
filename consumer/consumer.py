# from kafka import KafkaConsumer
# import json

# consumer = KafkaConsumer(
#     'stock-ticks',
#     bootstrap_servers='localhost:9092',
#     auto_offset_reset='earliest',
#     value_deserializer=lambda m: json.loads(m.decode('utf-8'))
# )

# for message in consumer:
#     tick = message.value
#     print(f"Received: {tick}")

from kafka import KafkaConsumer
import json
import logging
# import requests
import time

from analytics.moving_average import MovingAverageCalculator
from analytics.alerts import PriceAlert
from api.database import insert_record  # v3 database: updates cache + enqueues for DB

logging.basicConfig(filename='logs/analytics.log', level=logging.INFO, format='%(asctime)s - %(message)s')

consumer = KafkaConsumer(
    'stock-ticks',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    consumer_timeout_ms=1000  # so that the loop can be interrupted cleanly if needed
)

ma_calculator = MovingAverageCalculator(window_size=5)
price_alert = PriceAlert(threshold=3.0)

print("Consumer started. Waiting for messages...")

for message in consumer:
    try:
        tick = message.value
        symbol = tick['symbol']
        price = tick['price']
        timestamp = tick.get('timestamp', time.time())


        avg = ma_calculator.update(symbol, price)
        alert = price_alert.check(symbol, price)

        output = f"{symbol} | Price: {price} | MA(5): {avg:.2f}"
        print(output)
        logging.info(output)

        if alert:
            print(alert)
            logging.warning(alert)

    #     payload = {
    # "symbol": symbol,
    # "price": price,
    # "moving_average": round(avg, 2),
    # "alert": alert,
    # "timestamp": tick['timestamp']}

    # Directly insert record into database layer (this updates cache + enqueues for DB)
        insert_record(
            symbol=symbol,
            price=price,
            moving_average=round(avg, 2),
            alert=alert,
            timestamp=timestamp
        )

    except Exception as e:                              #Added logging and exception handling to avoid silent failure.
        logging.exception(f"Failed to process message: {e}")
