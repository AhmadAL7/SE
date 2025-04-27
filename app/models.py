from datetime import datetime
from app import db

role_permissions = db.Table('role_permissions',
    db.Column('id', db.Integer, primary_key=True, autoincrement=True),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id', ondelete="CASCADE")),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id', ondelete="CASCADE")),
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
    role_id = db.Column(db.Integer, db.ForeignKey('role.id', ondelete="RESTRICT"), nullable=False)
    staff = db.relationship('Staff', backref='user', lazy=True, uselist=False)

class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(15))
    email = db.Column(db.String(255))
    hire_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="RESTRICT"), nullable=False)
    schedules = db.relationship('StaffSchedule', backref='staff', lazy=True)
    requests = db.relationship('RequestTimeOff', backref='staff', lazy=True)
    notifications = db.relationship('Notification', backref='staff', lazy=True)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255))
    phone_number = db.Column(db.String(15))
    reservations = db.relationship('Reservation', backref='customer', lazy=True)
    supports = db.relationship('Support', backref='customer', lazy=True)
    reminder_logs = db.relationship('ReminderLog', backref='customer', lazy=True)

class TableModel(db.Model):
    __tablename__ = 'tables'
    id = db.Column(db.Integer, primary_key=True)
    table_number = db.Column(db.Integer, unique=True, nullable=False)
    seats = db.Column(db.Integer, nullable=False)
    orders = db.relationship("Order", backref="table", lazy=True)
    reservations = db.relationship("Reservation", backref="table", lazy=True)

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id', ondelete="RESTRICT"), nullable=False)
    reservation_time = db.Column(db.DateTime, nullable=False)
    number_of_people = db.Column(db.Integer, nullable=False)
    table_id = db.Column(db.Integer, db.ForeignKey('tables.id', ondelete="RESTRICT"), nullable=False)
    reminder_logs = db.relationship('ReminderLog', backref='reservation', lazy=True)

class Support(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id', ondelete="RESTRICT"), nullable=False)
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
    used_quantity = db.Column(db.Integer, nullable=False, default=0) 
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id', ondelete="RESTRICT"), nullable=False)

class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Numeric(10,2), nullable=False)
    description = db.Column(db.String(1000))
    order_links = db.relationship('OrderMenuItem', backref='menu', lazy=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, nullable=False)
    table_id = db.Column(db.Integer, db.ForeignKey('tables.id', ondelete="RESTRICT"), nullable=False)
    status = db.Column(db.String(255), nullable=False)
    total_price = db.Column(db.Numeric(10,2))
    payment_status = db.Column(db.String(255), nullable=False)
    menu_items = db.relationship('OrderMenuItem', backref='order', lazy=True)
    payments = db.relationship('Payment', backref='order', lazy=True)

class OrderMenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id', ondelete="RESTRICT"), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_item.id', ondelete="RESTRICT"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id', ondelete="RESTRICT"), nullable=False)
    payment_method = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Numeric(10,2), nullable=False)
    payment_date = db.Column(db.DateTime, nullable=False)

class RequestTimeOff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id', ondelete="CASCADE"), nullable=False)
    request_start = db.Column(db.DateTime)
    request_end = db.Column(db.DateTime)
    reason = db.Column(db.String(1000))
    status = db.Column(db.String(255))

class StaffSchedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id', ondelete="CASCADE"), nullable=False)
    shift_start = db.Column(db.DateTime)
    shift_end = db.Column(db.DateTime)

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id', ondelete="CASCADE"), nullable=True)

class ReminderLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id', ondelete="RESTRICT"), nullable=False)
    reservation_id = db.Column(db.Integer, db.ForeignKey('reservation.id', ondelete="CASCADE"), nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)