from flask import Blueprint, render_template

# Create a blueprint for  menu routes
menu_bp = Blueprint('menu', __name__)

@menu_bp.route('/')
def menu():
    from app.models import MenuItem  
    menu_items = MenuItem.query.all()  # Query the database for menu items
    return render_template('menu.html', menu_items=menu_items)