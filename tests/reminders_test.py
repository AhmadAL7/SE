# dummy_data/add_dummy_reservation.py

from datetime import datetime, timedelta
import pytz
from app import db, create_app
from app.models import Customer, Reservation, TableModel, ReminderLog
from app.logic.reservation_remind import Reservation_reminders

app = create_app()

def add_dummy_reservation():
    local_tz = pytz.timezone('Europe/London')
    now = datetime.now(local_tz)

    # Delete old ReminderLogs first
    old_reminders = ReminderLog.query.join(Customer).filter(Customer.email == "dummytester@example.com").all()
    for reminder in old_reminders:
        db.session.delete(reminder)
    db.session.commit()
    print("Old dummy reminder logs deleted.")

    # Delete old dummy reservation
    dummy_customer = Customer.query.filter_by(email="dummytester@example.com").first()
    if dummy_customer:
        old_reservations = Reservation.query.filter_by(customer_id=dummy_customer.id).all()
        for res in old_reservations:
            db.session.delete(res)
        db.session.delete(dummy_customer)
        db.session.commit()
        print("Old dummy reservations and customer deleted.")
 
    
    # Check if table already exists adn delete it 
    dummy_table = TableModel.query.filter_by(table_number=9999).first()
    if dummy_table:
        db.session.delete(dummy_table)
        db.session.commit()
        print("Old dummy table deleted.")



    # Create table
    table = TableModel(table_number=9999, seats=4)
    db.session.add(table)
    db.session.commit()
    print("Dummy table created.")
    
    # Create customer
    customer = Customer(
        first_name="Dummy",
        last_name="Tester",
        email="dummytester@example.com",
        phone_number="123456789")
    db.session.add(customer)
    db.session.commit()
    print("Dummy customer created.")

    # Create  reservation
    reservation_time = now + timedelta(hours=23, minutes=45)
    reservation = Reservation(
        customer_id=customer.id,
        reservation_time=reservation_time,
        number_of_people=2,
        table_id=table.id)
    db.session.add(reservation)
    db.session.commit()
    print(f"Dummy reservation created at {reservation_time}.")



    #tests
    print("Running send_reminders() test...")
    Reservation_reminders.send_reminders()

    # Check if ReminderLog was created
    reminder = ReminderLog.query.filter_by(customer_id=customer.id, reservation_id=reservation.id).first()
    if reminder:
        print("ReminderLog created successfully.")
    else:
        print("ReminderLog NOT created.")
if __name__ == "__main__":
    with app.app_context():
        add_dummy_reservation()
