
from app.logic.Inventory import InventoryLogic
from flask import render_template, request, redirect, url_for,Blueprint


inventory_bp = Blueprint('inventory', __name__)
# View inventory list
@inventory_bp.route('/inventory', methods=['GET'])
def inventory():
    inventory_items = InventoryLogic.get_all_inventory_items()
    return render_template('inventory.html', inventory_items=inventory_items)
# Update inventory item
@inventory_bp.route('/inventory/update/<int:item_id>', methods=['POST'])
def update_inventory_item(item_id):
    item_name = request.form.get('item_name')
    quantity = int(request.form.get('quantity'))
  
    
    InventoryLogic.update_inventory(item_id, item_name, quantity)
    return redirect(url_for('inventory.inventory'))


# Add inventory or supplier
@inventory_bp.route('/add_supplier_inventory', methods=['GET', 'POST'])
def add_supplier_inventory():
    if request.method == 'POST':
        if request.form.get('form_type') == 'supplier':
            # Supplier form submitted
            name = request.form.get('name')
            contact_info = request.form.get('contact_info')
            address = request.form.get('address')
            InventoryLogic.create_supplier(name, contact_info, address)

        elif request.form.get('form_type') == 'inventory':
            # Inventory form submitted
            item_name = request.form.get('item_name')
            quantity = int(request.form.get('quantity'))
            supplier_id = int(request.form.get('supplier_id'))
            InventoryLogic.create_inventory(item_name, quantity, supplier_id)

        return redirect(url_for('inventory.add_supplier_inventory'))
    
    suppliers = InventoryLogic.get_all_suppliers()
    return render_template('add_supplier_inventory.html', suppliers=suppliers)

# Delete inventory item
@inventory_bp.route('/inventory/delete/<int:item_id>', methods=['POST'])
def delete_inventory_item(item_id):
    InventoryLogic.delete_inventory_item(item_id)
    return redirect(url_for('inventory.inventory'))



