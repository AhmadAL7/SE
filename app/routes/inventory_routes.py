
from app.logic.Inventory import InventoryLogic
from flask import render_template, request, redirect, url_for,Blueprint


inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route('/inventory', methods=['GET'])
def inventory():
    inventory_items = InventoryLogic.get_all_inventory_items()
    return render_template('inventory.html', inventory_items=inventory_items)

@inventory_bp.route('/inventory/update/<int:item_id>', methods=['POST'])
def update_inventory_item(item_id):
    item_name = request.form.get('item_name')
    quantity = request.form.get('quantity')
    
    InventoryLogic.update_inventory(item_id, item_name, quantity)
    return redirect(url_for('inventory.inventory'))