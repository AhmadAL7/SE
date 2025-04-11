from app.logic.base_crud import BaseCRUD
from app.models import Inventory

class InventoryLogic(BaseCRUD):
    

        
    @staticmethod
    def get_all_inventory_items():
        return BaseCRUD.get_all(Inventory)
