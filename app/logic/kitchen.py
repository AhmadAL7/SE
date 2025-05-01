from app.logic.base_crud import BaseCRUD
from app.models import Order
from flask import jsonify 

class KitchenLogic(BaseCRUD):


    @staticmethod
    def get_kitchen_orders():
        # Get only orders that are not marked as Done
        return BaseCRUD.get_all_records_by_filter(Order, status='In Progress')

    @staticmethod
    def mark_order_done(order_id):
        BaseCRUD.update(Order, order_id, status='Done')


    @staticmethod
    def get_order_json():
        orders = KitchenLogic.get_kitchen_orders()
 

        results = []
        for order in orders:

            items = [{'description': item.menu.description, 'quantity': item.quantity}
                    for item in order.menu_items]

            results.append({
                'id': order.id,
                'total_price': float(order.total_price),
                'table_id': order.table_id,
                'items': items
            })

        return results