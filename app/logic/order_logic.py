
from app.models import TableModel, Order, OrderMenuItem
from app.logic.base_crud import BaseCRUD



class OrderLogic(BaseCRUD):



    @staticmethod
    def get_all_tables():
        return BaseCRUD.get_all(TableModel)
    
    @staticmethod
    def get_order_by_table_id(table_id ):
        order_record =  BaseCRUD.get_row(Order, table_id= table_id)
        if not order_record:
            return None
        
        order_items= []
        for item in order_record.menu_items:
            order_items.append({
                'Item_name': item.menu.description,
                'quantity' : item.quantity,   
                'price' : item.menu.price
                })
            
        return {
            "order_id": order_record.id,
            "table_id": order_record.table_id,
            "all_items": order_items,
        }    
        
    @staticmethod
    def get_table_by_id(table_id):
        return BaseCRUD.get_row(TableModel, id= table_id)

 
            