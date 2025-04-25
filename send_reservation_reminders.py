# send_reservation_reminders.py

from datetime import datetime, timedelta
import pytz

from app import create_app, db
from app.models import Reservation, Customer, ReminderLog
from app.utils.email_helper import send_email

def send_reminders():
    app = create_app()
    with app.app_context():
        # 🕒 Use local timezone (BST-aware)
        local_tz = pytz.timezone('Europe/London')
        now = datetime.now(local_tz)

        window_start = now + timedelta(hours=23, minutes=30)
        window_end = now + timedelta(hours=24, minutes=30)

        print(f"🔍 Searching for reservations between {window_start} and {window_end}")

        upcoming_reservations = db.session.query(Reservation, Customer)\
            .join(Customer, Reservation.customer_id == Customer.id)\
            .filter(Reservation.reservation_time >= window_start)\
            .filter(Reservation.reservation_time <= window_end)\
            .all()

        print(f"📅 Found {len(upcoming_reservations)} reservations")

        for reservation, customer in upcoming_reservations:
            already_sent = ReminderLog.query.filter_by(
                customer_id=customer.id,
                reservation_id=reservation.id
            ).first()

            if already_sent:
                print(f"⏩ Skipped duplicate reminder for {customer.email}")
                continue

            subject = "Reservation Reminder - Your Booking is Tomorrow"
            body = (
                f"Hi {customer.first_name},\n\n"
                f"This is a reminder that you have a reservation tomorrow at "
                f"{reservation.reservation_time.strftime('%Y-%m-%d %H:%M')} for "
                f"{reservation.number_of_people} guest(s).\n\n"
                f"Thanks for choosing our restaurant!"
            )

            send_email(customer.email, subject, body)

            reminder = ReminderLog(
                customer_id=customer.id,
                reservation_id=reservation.id,
                sent_at=datetime.now(local_tz)
            )
            db.session.add(reminder)
            db.session.commit()

            print(f"[✔️] Reminder sent to {customer.email} for {reservation.reservation_time}")

if __name__ == "__main__":
    send_reminders()