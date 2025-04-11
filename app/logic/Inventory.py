from app.logic.base_crud import BaseCRUD
from app.models import Inventory

class InventoryLogic(BaseCRUD):
    
    @staticmethod
    def get_inv_ids_names():
        inventories = BaseCRUD.get_all(Inventory)
        ids = [inv.id for inv in inventories]
        names = [inv.name for inv in inventories]
        return  ids, names
        
    @staticmethod
    def get_all_inventory_items():
        return BaseCRUD.get_all(Inventory)
