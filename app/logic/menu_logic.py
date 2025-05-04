from app.models import MenuItem
from app.logic.base_crud import BaseCRUD

class MenuLogic(BaseCRUD):
    def __init__(self):
       pass

    @staticmethod
    def get_all_menu_items():
        return BaseCRUD.get_all(MenuItem)

    @staticmethod
    def get_menu_item_by_id(menu_item_id):
        return BaseCRUD.get_by_id(MenuItem, menu_item_id)

   # Add new menu item 
    @staticmethod
    def add_menu_item(price, description):
        return BaseCRUD.create(MenuItem, price=price, description=description)
    
# pass the values if there is any other wise have them as none(none does not update)
# Update price or description
    @staticmethod
    def update_menu_item(menu_item_id, price=None, description=None):
        return BaseCRUD.update(MenuItem, menu_item_id, price=price, description=description)
# Delete menu item
    @staticmethod
    def delete_menu_item(menu_item_id):
        return BaseCRUD.delete(MenuItem, menu_item_id)
