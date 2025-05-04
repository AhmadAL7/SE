from datetime import datetime, timedelta
from app.models import Reservation, ReminderLog
from app.logic.base_crud import BaseCRUD  
from app.utils.email_helper import send_email

class Reservation_reminders(BaseCRUD):

    @staticmethod
    def send_reminders():
        # Get reservations happening in 24h +- 30min
        now = datetime.now()
        start = now + timedelta(hours=23, minutes=30)
        end = now + timedelta(hours=24, minutes=30)

        # Get all upcoming reservations between start and end
        upcoming_reservations = BaseCRUD.get_records_by_date_range(
            Reservation,
            Reservation.reservation_time,
            start_date=start,
            end_date=end
        )

        for reservation in upcoming_reservations:
            customer = reservation.customer 


            # Check if reminder already sent
            already_sent = BaseCRUD.get_all_records_by_filter(
                ReminderLog,
                customer_id=customer.id,
                reservation_id=reservation.id
            )
            if already_sent:
                continue  # Skip if reminder already sent

            # Send reminder email
            send_email(
                to=customer.email,
                subject="Reservation Reminder: Your Booking is Tomorrow",
                body=f"Hi {customer.first_name},\n\nThis is a reminder for your reservation tomorrow at {reservation.reservation_time.strftime('%H:%M')}.\n\nThank you!"
            )

            # Log the reminder
            BaseCRUD.create(
                ReminderLog,
                customer_id=customer.id,
                reservation_id=reservation.id,
                sent_at=now
            )
