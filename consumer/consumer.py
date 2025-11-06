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
from analytics.moving_average import MovingAverageCalculator
from analytics.alerts import PriceAlert

logging.basicConfig(filename='logs/analytics.log', level=logging.INFO, format='%(asctime)s - %(message)s')

consumer = KafkaConsumer(
    'stock-ticks',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

ma_calculator = MovingAverageCalculator(window_size=5)
price_alert = PriceAlert(threshold=3.0)

for message in consumer:
    tick = message.value
    symbol = tick['symbol']
    price = tick['price']

    avg = ma_calculator.update(symbol, price)
    alert = price_alert.check(symbol, price)

    output = f"{symbol} | Price: {price} | MA(5): {avg:.2f}"
    print(output)
    logging.info(output)

    if alert:
        print(alert)
        logging.warning(alert)
