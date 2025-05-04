from flask import Blueprint, render_template, request, redirect, url_for
from app.logic.order_logic import OrderLogic
from app.logic.payment.processor import PaymentProcessor
from app.logic.payment.fake_payment import FakePaymentStrategy

payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/pay/<int:table_id>', methods=['GET', 'POST'])
def process_payment(table_id): ### work on processing the payment pass the table get the order
    
    logic = OrderLogic(table_id)
    
    order = logic.get_order_details()
    order_id = order["order_id"]
    table = logic.get_table_by_id()
    total_price = order["total_price"]


    if request.method == 'POST':
        amount = float(request.form['amount'])
        processor = PaymentProcessor(FakePaymentStrategy()) # context 

        try:
            result = processor.process_payment(order_id, amount)
        except ValueError as e:
            # Order not found or invalid
            return render_template('payment.html',
                                   error=str(e),
                                   total_price=total_price,
                                   menu_items=order["all_items"],
                                   order_id=order_id,
                                   table_id=table_id,
                                   table_number=table.table_number)
         # amount is not enough
        if result["status"] == "Failed":
            return render_template('payment.html',
                                   order_id=order_id,
                                   table_number=table.table_number,
                                   menu_items=order["all_items"],
                                   total_price=total_price,
                                  table_id=table_id,
                                   error=result["message"])
        # payment is done
        return redirect(url_for('payment.payment_tables'))

    return render_template('payment.html',
                           order_id=order_id,
                           table_id=table_id,
                           table_number=table.table_number,
                           menu_items=order["all_items"],
                           total_price=total_price)
 
 
 # Show all unpaid tables 
@payment_bp.route('/payment_tables')
def payment_tables():
    tables = OrderLogic.get_all_tables()
    
    table_orders = []

    for table in tables:
        for order in table.orders:
            if order.payment_status != 'Paid':
                table_orders.append({
                    "table_number": table.table_number,
                    "table_id": table.id,
                    "order_id": order.id,
                    "total_price": float(order.total_price)
                })
                break # stop checking for more unpaid orders for the current table
    return render_template('payment_tables.html', tables=table_orders)