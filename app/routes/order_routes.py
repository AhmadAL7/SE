# orderroutes.py
from flask import Blueprint, render_template, request, redirect, url_for
from app.logic.order_logic import OrderLogic
from app.logic.base_crud import BaseCRUD
from app.models import TableModel

order_bp = Blueprint('order', __name__)
logic = OrderLogic()

@order_bp.route('/tables')
def view_tables():
    
    tables = logic.get_all_tables()
    return render_template('tablesview.html', tables=tables)

@order_bp.route('/table/<int:table_id>')
def table_order(table_id):
    order = logic.get_order_by_table_id(table_id)
# if no order?
    table = logic.get_table_by_id(table_id)
    table_number = table.table_number
    menu_items = order["all_items"]
    order_id = order["order_id"]
    return render_template('order.html',order_id = order_id,  menu_items=menu_items, table_number=table_number)












@order_bp.route('/add_to_order/<int:table_id>', methods=['POST'])
def add_to_order(table_id):
    order = logic.get_order_by_table(table_id)
    if not order:
        return redirect(url_for('order.table_order', table_id=table_id))

    menu_item_id = int(request.form['menu_item_id'])
    quantity = int(request.form['quantity'])

    logic.add_menu_item_to_order(order.id, menu_item_id, quantity)
    return redirect(url_for('order.table_order', table_id=table_id))
