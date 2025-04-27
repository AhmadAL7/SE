

from datetime import datetime, timedelta
import pytz
from app import db
from app.models import Reservation, Customer, ReminderLog
from app.logic.base_crud import BaseCRUD  
from app.utils.email_helper import send_email


class Reservation_reminders(BaseCRUD):
    
    @staticmethod
    def send_reminders():
        now = datetime.now(pytz.timezone('Europe/London'))
        start = now + timedelta(hours=23, minutes=30)
        end = now + timedelta(hours=24, minutes=30)
        
        

        # get all reservations between start and end
        upcoming_reservations = db.session.query(Reservation, Customer)\
            .join(Customer, Reservation.customer_id == Customer.id)\
            .filter(Reservation.reservation_time.between(start, end))\
            .all()

        for reservation, customer in upcoming_reservations:
            #  check if a reminder was already sent
            already_sent = BaseCRUD.get_all_records_by_filter(
                ReminderLog,
                customer_id=customer.id,
                reservation_id=reservation.id
            )

            if already_sent:
                continue  # Skip if reminder already sent

            # Send the reminder email
            send_email(
                to=customer.email,
                subject="Reservation Reminder:  Your Booking is Tomorrow",
                body=f"Hi {customer.first_name},\n\nThis is a reminder for your reservation tomorrow at {reservation.reservation_time.strftime('%H:%M')}.\n\nThank you!"
            )

            #  add a reminder log
            BaseCRUD.create(
                ReminderLog,
                customer_id=customer.id,
                reservation_id=reservation.id,
                sent_at=now
            )
