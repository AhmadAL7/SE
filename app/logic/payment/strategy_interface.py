class StrategyInterface:
    def pay(self, order_id, amount):
        raise NotImplementedError("Subclasses must implement this method")