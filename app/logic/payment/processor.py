
class PaymentProcessor:
    def __init__(self, strategy):
        self.strategy = strategy
    
    # call the strategy pay method
    def process_payment(self, order_id, amount):
        return self.strategy.pay(order_id, amount)    