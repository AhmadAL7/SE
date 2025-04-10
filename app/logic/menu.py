from app.models import MenuItem
from app.logic.base_crud import BaseCRUD

class MenuLogic(BaseCRUD):
    def __init__(self):
       pass

    @staticmethod
    def get_all_menu_items():
        """Override the base method for custom logic if needed."""
        return BaseCRUD.get_all(MenuItem)

    @staticmethod
    def get_menu_item_by_id(menu_item_id):
        """Override the base method for custom logic if needed."""
        return BaseCRUD.get_by_id(MenuItem, menu_item_id)

    @staticmethod
    def add_menu_item(price, description, inventory_id):
        """Use the base `create` method to add a menu item."""
        return BaseCRUD.create(MenuItem, price=price, description=description, inventory_id=inventory_id)

    @staticmethod
    def update_menu_item(menu_item_id, price=None, description=None, inventory_id=None):
        """Override the base `update` method if needed."""
        return BaseCRUD.update(MenuItem, menu_item_id, price=price, description=description, inventory_id=inventory_id)

    @staticmethod
    def delete_menu_item(menu_item_id):
        """Use the base `delete` method to remove a menu item."""
        return BaseCRUD.delete(MenuItem, menu_item_id)