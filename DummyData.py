# app/simple_dummy_data.py
from app import create_app, db
from app.models import Role, Permission, User, Staff, Customer, TableModel, Reservation
from app.models import Support, Supplier, Inventory, MenuItem, Order, OrderMenuItem, Payment
from app.models import RequestTimeOff, StaffSchedule, ReminderLog, Notification
from datetime import datetime
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():
    # Clear existing data properly
    db.session.query(ReminderLog).delete()
    db.session.query(Notification).delete()
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
    db.session.commit()

    # Create Permissions
    access_kitchen = Permission(permission_name="AccessKitchen")
    access_inventory = Permission(permission_name="AccessInventory")
    access_staff_data = Permission(permission_name="AccessStaffData")
    db.session.add_all([access_kitchen, access_inventory, access_staff_data])
    db.session.commit()

    # Create Roles
    boh = Role(role_name="BOH")
    foh = Role(role_name="FOH")
    management = Role(role_name="Management")
    db.session.add_all([boh, foh, management])
    db.session.commit()

    # Assign permissions to roles
    boh.permissions.extend([access_kitchen, access_inventory])
    foh.permissions.append(access_kitchen)
    management.permissions.extend([access_kitchen, access_inventory, access_staff_data])
    db.session.commit()

    # Create Users
    chef_user = User(username="chef1", password=generate_password_hash("password123"), role_id=boh.id)
    server_user = User(username="server1", password=generate_password_hash("password123"), role_id=foh.id)
    manager_user = User(username="manager1", password=generate_password_hash("password123"), role_id=management.id)
    db.session.add_all([chef_user, server_user, manager_user])
    db.session.commit()

    # Create Staff linked to Users
    chef_staff = Staff(first_name="Gordon", last_name="Ramsay", phone_number="555-111-2222", email="gordon@kitchen.com", hire_date=datetime(2023, 1, 15), user_id=chef_user.id)
    server_staff = Staff(first_name="Emily", last_name="Clark", phone_number="555-333-4444", email="emily@restaurant.com", hire_date=datetime(2023, 2, 10), user_id=server_user.id)
    manager_staff = Staff(first_name="Olivia", last_name="Smith", phone_number="555-555-6666", email="olivia@restaurant.com", hire_date=datetime(2022, 11, 20), user_id=manager_user.id)
    db.session.add_all([chef_staff, server_staff, manager_staff])
    db.session.commit()

    # Create Customers
    customer1 = Customer(first_name="John", last_name="Doe", email="john.doe@email.com", phone_number="555-777-8888")
    customer2 = Customer(first_name="Jane", last_name="Smith", email="jane.smith@email.com", phone_number="555-888-9999")
    db.session.add_all([customer1, customer2])
    db.session.commit()

    # Create Tables
    table1 = TableModel(table_number=1, seats=2)
    table2 = TableModel(table_number=2, seats=4)
    db.session.add_all([table1, table2])
    db.session.commit()

    # Create Reservations
    reservation1 = Reservation(customer_id=customer1.id, reservation_time=datetime(2025, 5, 10, 19, 0), number_of_people=2, table_id=table1.id)
    reservation2 = Reservation(customer_id=customer2.id, reservation_time=datetime(2025, 5, 11, 20, 0), number_of_people=4, table_id=table2.id)
    db.session.add_all([reservation1, reservation2])
    db.session.commit()

    # Create Reminder Logs
    reminder1 = ReminderLog(customer_id=customer1.id, reservation_id=reservation1.id)
    reminder2 = ReminderLog(customer_id=customer2.id, reservation_id=reservation2.id)
    db.session.add_all([reminder1, reminder2])
    db.session.commit()

    # Create Support inquiries
    support1 = Support(email="john33.doe@email.com", inquiry_date=datetime(2025, 5, 5), inquiry_text="Can I change my table?")
    db.session.add(support1)
    db.session.commit()

    # Create Suppliers
    supplier1 = Supplier(name="Fresh Farm Produce", contact_info="contact@farm.com", address="123 Farm Road")
    supplier2 = Supplier(name="Seafood Delights", contact_info="seafood@sea.com", address="456 Ocean Avenue")
    db.session.add_all([supplier1, supplier2])
    db.session.commit()

    # Create Inventory Items
    inventory1 = Inventory(item_name="Tomatoes", quantity=100, used_quantity=20, supplier_id=supplier1.id)
    inventory2 = Inventory(item_name="Salmon", quantity=50, used_quantity=5, supplier_id=supplier2.id)
    db.session.add_all([inventory1, inventory2])
    db.session.commit()

    # Create Menu Items
    menu_item1 = MenuItem(price=12.99, description="Fresh Garden Salad")
    menu_item2 = MenuItem(price=24.99, description="Grilled Salmon Plate")
    db.session.add_all([menu_item1, menu_item2])
    db.session.commit()

    # Create Orders
    order1 = Order(order_date=datetime(2025, 5, 6), table_id=table1.id, status="Completed", total_price=37.98, payment_status="Paid")
    db.session.add(order1)
    db.session.commit()

    # Create Order Menu Items
    order_menu_item1 = OrderMenuItem(order_id=order1.id, menu_item_id=menu_item1.id, quantity=1)
    order_menu_item2 = OrderMenuItem(order_id=order1.id, menu_item_id=menu_item2.id, quantity=1)
    db.session.add_all([order_menu_item1, order_menu_item2])
    db.session.commit()

    # Create Payment
    payment1 = Payment(order_id=order1.id, payment_method="Credit Card", amount=37.98, payment_date=datetime(2025, 5, 6, 21, 0))
    db.session.add(payment1)
    db.session.commit()

    # Create Staff Schedules
    schedule1 = StaffSchedule(staff_id=chef_staff.id, shift_start=datetime(2025, 5, 10, 8, 0), shift_end=datetime(2025, 5, 10, 16, 0))
    db.session.add(schedule1)
    db.session.commit()

    # Create Time-Off Requests
    timeoff1 = RequestTimeOff(staff_id=server_staff.id, request_start=datetime(2025, 5, 15), request_end=datetime(2025, 5, 16), reason="Family event", status="Approved")
    db.session.add(timeoff1)
    db.session.commit()

    print("dummy data created!")
