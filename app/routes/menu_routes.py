
from flask import render_template, request, redirect, url_for,Blueprint

from app.logic.menu_logic import MenuLogic
from app.logic.Inventory import InventoryLogic

menu_bp = Blueprint('menu', __name__)
# Display the menu page with all menu items
@menu_bp.route('/menu')
def menu():
    menu_items = MenuLogic.get_all_menu_items()
    return render_template('menu.html', menu_items=menu_items)

# adding a new menu item
@menu_bp.route('/menu/add', methods=['GET', 'POST'])
def add_menu_item():
    if request.method == 'POST':

        description = request.form.get('description')
        price = float(request.form.get('price'))

        MenuLogic.add_menu_item(price, description)
        return redirect(url_for('menu.menu'))  # Redirect back to the menu page after adding item.

    
    return render_template('menu_add.html')  # Render the form with inventories