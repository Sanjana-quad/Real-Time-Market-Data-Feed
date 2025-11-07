class PriceAlert:
    def __init__(self, threshold=3.0):  # percentage threshold
        self.last_price = {}
        self.threshold = threshold

    def check(self, symbol, new_price):
        if symbol not in self.last_price:
            self.last_price[symbol] = new_price
            return None

        old_price = self.last_price[symbol]
        change_percent = ((new_price - old_price) / old_price) * 100
        self.last_price[symbol] = new_price

        if abs(change_percent) >= self.threshold:
            return f"⚠️ {symbol} changed by {change_percent:.2f}%"
        return None
    
    