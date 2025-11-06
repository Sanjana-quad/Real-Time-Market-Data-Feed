import pandas as pd
from collections import deque

class MovingAverageCalculator:
    def __init__(self, window_size=5):
        self.window_size = window_size
        self.data = {}  # symbol -> deque

    def update(self, symbol, price):
        if symbol not in self.data:
            self.data[symbol] = deque(maxlen=self.window_size)
        self.data[symbol].append(price)
        df = pd.Series(self.data[symbol])
        return df.mean()
