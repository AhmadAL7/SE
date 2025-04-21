# app/models.py
from app import db



role_permissions = db.Table('role_permissions',
    db.Column('id', db.Integer, primary_key=True, autoincrement=True),  # Auto-incrementing primary key
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'))
)

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(255), unique=True, nullable=False)
    users = db.relationship('User', backref='role', lazy=True)
    permissions = db.relationship('Permission', secondary=role_permissions, backref=db.backref('roles', lazy=True))

class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    permission_name = db.Column(db.String(255), unique=True, nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    staff = db.relationship('Staff', backref='user', lazy=True, uselist=False)

class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(15))
    email = db.Column(db.String(255))
    hire_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255))
    phone_number = db.Column(db.String(15))
    reservations = db.relationship('Reservation', backref='customer', lazy=True)
    supports = db.relationship('Support', backref='customer', lazy=True)

class TableModel(db.Model):
    __tablename__ = 'tables' # use this name not the tablemodel in the database
    id = db.Column(db.Integer, primary_key=True)
    table_number = db.Column(db.Integer, unique=True, nullable=False)
    seats = db.Column(db.Integer, nullable=False)

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    reservation_time = db.Column(db.DateTime, nullable=False)
    number_of_people = db.Column(db.Integer, nullable=False)
    table_id = db.Column(db.Integer, db.ForeignKey('tables.id'))

class Support(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    inquiry_date = db.Column(db.DateTime)
    inquiry_text = db.Column(db.Text)

class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    contact_info = db.Column(db.String(255))
    address = db.Column(db.String(255))
    inventory_items = db.relationship('Inventory', backref='supplier', lazy=True)

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))
    menu_items = db.relationship('MenuItem', backref='inventory', lazy=True)

class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Numeric(10,2), nullable=False)
    description = db.Column(db.String(1000))
    inventory_id = db.Column(db.Integer, db.ForeignKey('inventory.id'))

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, nullable=False)
    table_id = db.Column(db.Integer, db.ForeignKey('tables.id'))
    status = db.Column(db.String(255), nullable=False)
    total_price = db.Column(db.Numeric(10,2))
    payment_status = db.Column(db.String(255), nullable=False)
    menu_items = db.relationship('OrderMenuItem', backref='order', lazy=True)

class OrderMenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_item.id'))
    quantity = db.Column(db.Integer, nullable=False)
    menu = db.relationship('MenuItem', backref='order_links')


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    payment_method = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Numeric(10,2), nullable=False)
    payment_date = db.Column(db.DateTime, nullable=False)

class RequestTimeOff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'))
    request_start = db.Column(db.DateTime)
    request_end = db.Column(db.DateTime)
    reason = db.Column(db.String(1000))
    status = db.Column(db.String(255))

class StaffSchedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'))
    shift_start = db.Column(db.DateTime)
    shift_end = db.Column(db.DateTime)

class WebReservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(10), nullable=False)
    guests = db.Column(db.Integer, nullable=False)

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # 'FOH', 'BOH', or 'Manager'
    timestamp = db.Column(db.DateTime)
