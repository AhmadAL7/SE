# app/simple_dummy_data.py
from app import create_app, db
from app.models import Role, Permission, User, Staff, Customer, TableModel, Reservation
from app.models import Support, Supplier, Inventory, MenuItem, Order, OrderMenuItem, Payment
from app.models import RequestTimeOff, StaffSchedule
from datetime import datetime
from werkzeug.security import generate_password_hash


app = create_app()
with app.app_context():
    # Clear existing data 
    db.session.query(StaffSchedule).delete()
    db.session.query(RequestTimeOff).delete()
    db.session.query(Payment).delete()
    db.session.query(OrderMenuItem).delete()
    db.session.query(Order).delete()
    db.session.query(MenuItem).delete()
    db.session.query(Inventory).delete()
    db.session.query(Supplier).delete()
    db.session.query(Support).delete()
    db.session.query(Reservation).delete()
    db.session.query(TableModel).delete()
    db.session.query(Customer).delete()
    db.session.query(Staff).delete()
    db.session.query(User).delete()
    db.session.query(Role).delete()
    db.session.query(Permission).delete()

    # Create Permissions
    access_kitchen = Permission(permission_name="AccessKitchen")
    access_inventory = Permission(permission_name="AccessInventory")
    access_staff_data = Permission(permission_name="AccessStaffData")

    db.session.add(access_kitchen)
    db.session.add(access_inventory)
    db.session.add(access_staff_data)
    db.session.commit()

    # Create Roles
    boh = Role(role_name="BOH")
    foh = Role(role_name="FOH")
    management = Role(role_name="Management")

    db.session.add(boh)
    db.session.add(foh)
    db.session.add(management)
    db.session.commit()
    
    foh.permissions.extend([access_kitchen])
    boh.permissions.extend([access_inventory, access_kitchen])
    management.permissions.extend([access_staff_data, access_inventory, access_kitchen])
    db.session.commit()
    # Create Users
    chef_user = User(username="chef1", password=generate_password_hash("password123"), role_id=boh.id)
    server_user = User(username="server1", password=generate_password_hash("password123"), role_id=foh.id)
    manager_user = User(username="manager1", password=generate_password_hash("password123"), role_id=management.id)

    db.session.add(chef_user)
    db.session.add(server_user)
    db.session.add(manager_user)
    db.session.commit()

    # Create Staff
    chef_staff = Staff(first_name="Gordon", last_name="Ramsay", phone_number="555-123-4567", email="chef@restaurant.com", hire_date=datetime(2023, 1, 15), user_id=chef_user.id)
    server_staff = Staff(first_name="Emily", last_name="Johnson", phone_number="555-456-7890", email="server@restaurant.com", hire_date=datetime(2023, 1, 5), user_id=server_user.id)
    manager_staff = Staff(first_name="David", last_name="Lee", phone_number="555-789-0123", email="manager@restaurant.com", hire_date=datetime(2022, 11, 10), user_id=manager_user.id)

    db.session.add(chef_staff)
    db.session.add(server_staff)
    db.session.add(manager_staff)
    db.session.commit()

    # Create Tables
    table1 = TableModel(table_number=1, seats=2)
    table2 = TableModel(table_number=2, seats=2)
    table3 = TableModel(table_number=3, seats=4)
    table4 = TableModel(table_number=4, seats=6)

    db.session.add(table1)
    db.session.add(table2)
    db.session.add(table3)
    db.session.add(table4)
    db.session.commit()

    # Create Customers
    customer1 = Customer(first_name="John", last_name="Doe", email="john.doe@email.com", phone_number="555-111-2222")
    customer2 = Customer(first_name="Jane", last_name="Smith", email="jane.smith@email.com", phone_number="555-222-3333")
    customer3 = Customer(first_name="Robert", last_name="Johnson", email="robert.j@email.com", phone_number="555-333-4444")

    db.session.add(customer1)
    db.session.add(customer2)
    db.session.add(customer3)
    db.session.commit()

    # Create Reservations
    reservation1 = Reservation(customer_id=customer1.id, reservation_time=datetime(2025, 4, 6, 18, 0), number_of_people=2, table_id=table1.id)
    reservation2 = Reservation(customer_id=customer2.id, reservation_time=datetime(2025, 4, 7, 19, 30), number_of_people=4, table_id=table3.id)
    reservation3 = Reservation(customer_id=customer3.id, reservation_time=datetime(2025, 4, 8, 20, 0), number_of_people=6, table_id=table4.id)

    db.session.add(reservation1)
    db.session.add(reservation2)
    db.session.add(reservation3)
    db.session.commit()

    # Create Support inquiries
    support1 = Support(customer_id=customer1.id, inquiry_date=datetime(2025, 4, 1), inquiry_text="I need to change my reservation time.")
    support2 = Support(customer_id=customer2.id, inquiry_date=datetime(2025, 4, 2), inquiry_text="Do you offer vegetarian options?")

    db.session.add(support1)
    db.session.add(support2)
    db.session.commit()

    # Create Suppliers
    supplier1 = Supplier(name="Farm Fresh Produce", contact_info="contact@farmfresh.com", address="123 Farm Road")
    supplier2 = Supplier(name="Quality Meats", contact_info="sales@qualitymeats.com", address="456 Butcher Street")
    supplier3 = Supplier(name="Seafood Direct", contact_info="orders@seafood.com", address="789 Harbor Drive")

    db.session.add(supplier1)
    db.session.add(supplier2)
    db.session.add(supplier3)
    db.session.commit()

    # Create Inventory items
    inventory1 = Inventory(item_name="Tomatoes", quantity=50, supplier_id=supplier1.id)
    inventory2 = Inventory(item_name="Beef", quantity=20, supplier_id=supplier2.id)
    inventory3 = Inventory(item_name="Salmon", quantity=15, supplier_id=supplier3.id)

    db.session.add(inventory1)
    db.session.add(inventory2)
    db.session.add(inventory3)
    db.session.commit()

    # Create Menu Items
    menu_item1 = MenuItem(price=12.99, description="Fresh garden salad", inventory_id=inventory1.id)
    menu_item2 = MenuItem(price=18.99, description="Beef burger with fries", inventory_id=inventory2.id)
    menu_item3 = MenuItem(price=22.99, description="Salmon fillet with vegetables", inventory_id=inventory3.id)

    db.session.add(menu_item1)
    db.session.add(menu_item2)
    db.session.add(menu_item3)
    db.session.commit()

    # Create Orders
    order1 = Order(order_date=datetime(2025, 4, 4), table_id=table1.id, status="Completed", total_price=31.98, payment_status="Paid")
    order2 = Order(order_date=datetime(2025, 4, 5), table_id=table2.id, status="In Progress", total_price=18.99, payment_status="Pending")

    db.session.add(order1)
    db.session.add(order2)
    db.session.commit()

    # Create Order Menu Items
    order_item1 = OrderMenuItem(order_id=order1.id, menu_item_id=menu_item1.id, quantity=1)
    order_item2 = OrderMenuItem(order_id=order1.id, menu_item_id=menu_item2.id, quantity=1)
    order_item3 = OrderMenuItem(order_id=order2.id, menu_item_id=menu_item2.id, quantity=1)

    db.session.add(order_item1)
    db.session.add(order_item2)
    db.session.add(order_item3)
    db.session.commit()

    # Create Payments
    payment1 = Payment(order_id=order1.id, payment_method="Credit Card", amount=31.98, payment_date=datetime(2025, 4, 4, 20, 30))

    db.session.add(payment1)
    db.session.commit()

    # Create Staff Schedules
    schedule1 = StaffSchedule(staff_id=chef_staff.id, shift_start=datetime(2025, 4, 6, 8, 0), shift_end=datetime(2025, 4, 6, 16, 0))
    schedule2 = StaffSchedule(staff_id=server_staff.id, shift_start=datetime(2025, 4, 6, 16, 0), shift_end=datetime(2025, 4, 6, 22, 0))
    schedule3 = StaffSchedule(staff_id=manager_staff.id, shift_start=datetime(2025, 4, 6, 10, 0), shift_end=datetime(2025, 4, 6, 19, 0))

    db.session.add(schedule1)
    db.session.add(schedule2)
    db.session.add(schedule3)
    db.session.commit()

    # Create Time-Off Requests
    time_off1 = RequestTimeOff(staff_id=chef_staff.id, request_start=datetime(2025, 4, 15), request_end=datetime(2025, 4, 17), reason="Vacation", status="Approved")
    time_off2 = RequestTimeOff(staff_id=server_staff.id, request_start=datetime(2025, 4, 20), request_end=datetime(2025, 4, 20), reason="Doctor's appointment", status="Pending")

    db.session.add(time_off1)
    db.session.add(time_off2)
    db.session.commit()

    print("Dummy data created successfully!")