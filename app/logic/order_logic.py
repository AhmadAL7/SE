
from app.models import TableModel, Order, OrderMenuItem
from app.logic.base_crud import BaseCRUD



class OrderLogic(BaseCRUD):

    def __init__(self, tabel_id):
        self.table_id = tabel_id  # set the table id
        self.order = BaseCRUD.get_row(Order, table_id= self.table_id)  # get the order
        if not self.order: # if it doesnt exists createa  new one and assign it order name
            from datetime import datetime
            BaseCRUD.create(Order, table_id=self.table_id, order_date=datetime.now(), status='In Progress', total_price=0.0, payment_status='Pending')
            self.order = BaseCRUD.get_row(Order, table_id=self.table_id)
   # gets all tables
    @staticmethod
    def get_all_tables():
        return BaseCRUD.get_all(TableModel)
    
    # gets all order details(used in the routes to access prices, names and other info)
    def get_order_details(self):
        order_items= []
        for item in self.order.menu_items:
            order_items.append({
                'Item_name': item.menu.description,
                'quantity' : item.quantity,   
                'price' : item.menu.price,
                'id':item.menu.id
                })
            
        return {
            "order_id": self.order.id,
            "table_id": self.order.table_id,
            "all_items": order_items,
            "total_price": self.order.total_price
        }    
        
    
    def get_table_by_id(self):
        return BaseCRUD.get_row(TableModel, id= self.table_id)


    def add_menu_item(self, menu_item_id, quantity):
        existing = BaseCRUD.get_row(OrderMenuItem, order_id=self.order.id, menu_item_id=menu_item_id) # check if the item already exists

        if existing: # if it exists update the quantity
            new_quantity = existing.quantity + quantity
            BaseCRUD.update(OrderMenuItem, existing.id, quantity=new_quantity)
        else: # if it doesnt exist create a new one
            BaseCRUD.create(OrderMenuItem, order_id=self.order.id, menu_item_id=menu_item_id, quantity=quantity)
        # update the total price of the order
        self.update_total_price()


    def update_total_price(self):
        total = 0
        for item in self.order.menu_items: # go through all the items for the order through(ordermenuitem model)
            total += float(item.menu.price * item.quantity) # add the price of each item to the total(multiplying the quantity)
        BaseCRUD.update(Order, self.order.id, total_price=total) # update the total price of the order in the order model
        self.order.total_price = total  # updating the local reference of order (in case of useing it in the routes)
        return total
    
    def remove_order(self):
        for item in self.order.menu_items: # go through all the items relating to the order in the OrderMenuItem model and delete them
            BaseCRUD.delete(OrderMenuItem, item.id)
        BaseCRUD.delete(Order, self.order.id) # delete the order record
        return True

    

    def decrease_quantity(self, menu_item_id, quantity):
        item = BaseCRUD.get_row(OrderMenuItem, order_id=self.order.id, menu_item_id=menu_item_id) # get the item from the ordermenuitem model
        if not item:
            return None

        if item.quantity > quantity: # if the current quantity is more than 1
            new_quantity = item.quantity - quantity
            BaseCRUD.update(OrderMenuItem, item.id, quantity=new_quantity) # update the quantity in the ordermenuitem model
        else:
            BaseCRUD.delete(OrderMenuItem, item.id) # delete if the quantity is 0

        remaining_items = BaseCRUD.get_row(OrderMenuItem, order_id= self.order.id)
        if not remaining_items:
            BaseCRUD.delete(Order, self.order.id)
            return "deleted"

        self.update_total_price()
        return True
    
    def get_order_by_table_id(self):
        return BaseCRUD.get_row(Order, table_id=self.table_id)