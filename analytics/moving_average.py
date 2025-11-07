from collections import deque, defaultdict

class MovingAverageCalculator:
    def __init__(self, window_size=5):
        self.window_size = window_size
        self.prices = defaultdict(lambda: deque(maxlen=window_size))

    def update(self, symbol, price):
        self.prices[symbol].append(price)
        return sum(self.prices[symbol]) / len(self.prices[symbol])
