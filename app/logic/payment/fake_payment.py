from app.logic.payment.strategy_interface import StrategyInterface

from app.logic.base_crud import BaseCRUD
from datetime import datetime, timezone
from flask import Blueprint

payment_bp = Blueprint('payment', __name__)


class FakePaymentStrategy(StrategyInterface):
    
    def pay(self, order_id, amount):
        from app.models import Payment, Order
        order = BaseCRUD.get_row(Order, id=order_id)

        if not order:
            raise ValueError("Order not found")

        
        #check if the amount is enough
        total_price = order.total_price
        if amount < total_price:
            return {
                "status": "Failed",
                "message": f"Required amount: {total_price}"
            }
        # mark the order as paid
        BaseCRUD.update(Order,id = order_id , payment_status='Paid')
        
        # log the payment
        BaseCRUD.create(
            Payment,
            order_id=order_id,
            amount=amount,
            payment_method="Fake",
            payment_date=datetime.now(timezone.utc)
        )
        


        
        return {
            "status": "Success",
            "order_id": order_id,
            "amount_paid": amount,
            "message": "Payment processed successfully (fake)"
        }