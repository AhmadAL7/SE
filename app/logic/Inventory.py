from app.logic.base_crud import BaseCRUD
from app.models import Inventory, Supplier

class InventoryLogic(BaseCRUD):
    

       # Get all inventory items 
    @staticmethod
    def get_all_inventory_items():
        return BaseCRUD.get_all(Inventory)
    
    # Update item quantity and track used quantity
    @staticmethod
    def update_inventory(id, name, new_quantity):
        inventory_item = Inventory.query.get(id)
        new_quantity = float(new_quantity)
        if not inventory_item:
            return None
        
        updated_item_name = name
        updated_quantity = new_quantity
        updated_used_quantity = inventory_item.used_quantity
        

        #  if quantity decreased, update used_quantity
        if new_quantity < inventory_item.quantity:
            used_change = inventory_item.quantity - new_quantity
            updated_used_quantity += used_change
        return BaseCRUD.update(
        Inventory,
        id,item_name=updated_item_name,quantity=updated_quantity,used_quantity=updated_used_quantity)

    # Get items with quantity below threshold
    @staticmethod
    def get_low_stock_items(threshold=5):
        return Inventory.query.filter(Inventory.quantity < threshold).all()
    # Add new inventory item
    @staticmethod
    def create_inventory(item_name, quantity, supplier_id):
        return BaseCRUD.create(Inventory, item_name=item_name, quantity=quantity, used_quantity=0, supplier_id=supplier_id)

    #supplier
    # Create new supplier
    @staticmethod
    def create_supplier(name, contact_info, address):
        return BaseCRUD.create(Supplier, name=name, contact_info=contact_info, address=address)
    # Get all suppliers
    @staticmethod
    def get_all_suppliers():
        return BaseCRUD.get_all(Supplier)
    # Delete an inventory item
    @staticmethod
    def delete_inventory_item(id):
        return BaseCRUD.delete(Inventory, id)
