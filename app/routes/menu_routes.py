
from flask import render_template, request, redirect, url_for,Blueprint

from app.logic.menu_logic import MenuLogic
from app.logic.Inventory import InventoryLogic

menu_bp = Blueprint('menu', __name__)

@menu_bp.route('/')
def menu():
    menu_items = MenuLogic.get_all_menu_items()
    return render_template('menu.html', menu_items=menu_items)

@menu_bp.route('/menu/add', methods=['GET', 'POST'])
def add_menu_item():
    if request.method == 'POST':
        inventory_id = request.form.get('inventory_id')
        description = request.form.get('description')
        price = float(request.form.get('price'))

        MenuLogic.add_menu_item(price=price, description=description, inventory_id=inventory_id)
        return redirect(url_for('menu.menu'))  # Redirect back to the menu page after adding item.

    # GET method - show form
    inventories = InventoryLogic.get_all_inventory_items() # Get all inventory items
    return render_template('menu_add.html', inventories=inventories)  # Render the form with inventories