# orderroutes.py
from flask import Blueprint, render_template, request, redirect, url_for
from app.logic.order_logic import OrderLogic
from app.logic.base_crud import BaseCRUD
from app.models import TableModel
from app.logic.menu_logic import MenuLogic
from app.logic.kitchen import KitchenLogic

from flask import jsonify 
order_bp = Blueprint('order', __name__)


# view tables
@order_bp.route('/tables')
def view_tables():
    
    tables = OrderLogic.get_all_tables()
    return render_template('tablesview.html', tables=tables)

# view order table
@order_bp.route('/table/<int:table_id>')
def table_order(table_id):
    logic = OrderLogic(table_id)
    order = logic.get_order_details() # get order details

    table = logic.get_table_by_id() # get table details
    table_number = table.table_number
    menu_items = order["all_items"]
    order_id = order["order_id"]
    total_price = order["total_price"]
    
    all_menu_items = MenuLogic.get_all_menu_items() # get all menu items for selcting items to add to order
    
    return render_template('order.html', order_id=order_id, menu_items=menu_items, table_number=table_number, table_id=table_id, all_menu_items = all_menu_items, total_price = total_price)




@order_bp.route('/add_to_order/<int:table_id>', methods=['POST'])
def add_to_order(table_id):
    logic = OrderLogic(table_id)

    
    menu_item_id = int(request.form['menu_item_id'])
    quantity = int(request.form['quantity'])

    logic.add_menu_item( menu_item_id, quantity) # add menu item to order/ increase quantity
    total_price = logic.order.total_price 
    return redirect(url_for('order.table_order', table_id=table_id, total_price = total_price))


@order_bp.route('/remove_order/<int:table_id>', methods=['POST'])
def remove_order(table_id):
    logic = OrderLogic(table_id)

    logic.remove_order()
    return redirect(url_for('order.view_tables', table_id=table_id)) # send to the tables page after removal
    
@order_bp.route('/decrease/<int:table_id>/<int:menu_item_id>', methods=['POST'])
def decrease_quantity(table_id, menu_item_id):
    
    logic = OrderLogic(table_id)

    result = logic.decrease_quantity( menu_item_id, quantity=1)  
    
    if result == "deleted":
       # order has no items and deleted redirect to the tables
        return redirect(url_for('order.view_tables'))
        
    return redirect(url_for('order.table_order', table_id=table_id))

#Kichen
@order_bp.route('/kitchen')
def kitchen_view():
    from app.models import Order
    orders = KitchenLogic.get_kitchen_orders()
    return render_template('kitchen.html', orders=orders)


@order_bp.route('/mark_done/<int:order_id>', methods=['POST'])
def mark_order_done(order_id):
    KitchenLogic.mark_order_done(order_id)

    return redirect(url_for('order.kitchen_view'))

@order_bp.route('/kitchen/orders/json')
def kitchen_orders_json():
    details = KitchenLogic.get_order_json()
    return jsonify(details)


