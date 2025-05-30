from app.models import Reservation, TableModel, Customer
from app.logic.base_crud import BaseCRUD
from app.logic.reservation_factory import ReservationFactory
from app.utils.email_helper import send_email
from app import db
from datetime import datetime, timedelta
import pytz

class ReservationLogic(BaseCRUD):
    def __init__(self):
        pass
# Create a reservation with validation
    @staticmethod
    def create_reservation(form_data):
        name = form_data.get('name')
        email = form_data.get('email')
        phone = form_data.get('phone')
        date = form_data.get('date')
        time = form_data.get('time')
        guests = int(form_data.get('guests'))

        print(f"[LOGIC] Reservation Attempt: {name} | {email} | {phone} | {date} {time} | {guests} guests")

        reservation_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")

        # Apply BST timezone
        local_tz = pytz.timezone("Europe/London")
        reservation_datetime = local_tz.localize(reservation_datetime)
        now = datetime.now(local_tz)
        # Time validation
        if reservation_datetime <= now:
            raise ValueError("Reservation must be for a future time.")
        if reservation_datetime - now < timedelta(hours=24):
            raise ValueError("Reservations must be made at least 24 hours in advance.")
        
        # Split full name into first and last
        parts = name.strip().split()
        first_name = parts[0]
        last_name = parts[1] if len(parts) > 1 else ""
       # Find or create customer 
        customer = Customer.query.filter_by(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone
        ).first()

        if not customer:
            customer = Customer(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone
            )
            db.session.add(customer)
            db.session.commit()
         # Prevent duplicate reservations
        existing_booking = Reservation.query.filter_by(
            customer_id=customer.id,
            reservation_time=reservation_datetime
        ).first()
        if existing_booking:
            raise ValueError("You already have a reservation at this time.")
       # Create reservation using factory
        reservation = ReservationFactory.create_reservation(
            customer_id=customer.id,
            reservation_time=reservation_datetime,
            guests=guests
        )

        if not reservation:
            raise ValueError("No available tables for that time or guest count.")

        db.session.add(reservation)
        db.session.commit()

        # send confirmation email
        try:
            send_email(
                to_email=customer.email,
                subject="Reservation Confirmed",
                message_body=(
                    f"Dear {customer.first_name},\n\n"
                    f"Your reservation has been confirmed for {reservation_datetime.strftime('%Y-%m-%d at %H:%M')} "
                    f"for {guests} guest(s).\n\nThank you!"
                )
            )
        except Exception as e:
            print(f"[EMAIL ERROR] Failed to send confirmation email: {e}")

        return reservation
# Get all reservations
    @staticmethod
    def get_all_reservations():
        return BaseCRUD.get_all(Reservation)
# Get reservations with customer details
    @staticmethod
    def get_all_reservations_with_customer():
        return db.session.query(Reservation, Customer)\
            .join(Customer, Reservation.customer_id == Customer.id).all()
# Get reservation by ID
    @staticmethod
    def get_reservation_by_id(reservation_id):
        return BaseCRUD.get_by_id(Reservation, reservation_id)
# Update reservation with validation checks
    @staticmethod
    def update_reservation_with_validation(reservation_id, form_data):
        reservation = Reservation.query.get(reservation_id)
        if not reservation:
            return None, "Reservation not found."

        try:
            new_guest_count = int(form_data.get('guests'))
            new_date = form_data.get('date')
            new_time = form_data.get('time')
            new_datetime = datetime.strptime(f"{new_date} {new_time}", "%Y-%m-%d %H:%M")

            local_tz = pytz.timezone("Europe/London")
            new_datetime = local_tz.localize(new_datetime)
            now = datetime.now(local_tz)

            # Validation 1:in the future
            if new_datetime <= now:
                return None, "Reservation must be in the future."

            # validation 2:  24 hours ahead
            if new_datetime - now < timedelta(hours=24):
                return None, "Reservations must be made at least 24 hours in advance."

            # validation 3: between 12:00 and 22:00
            if not (datetime.strptime("12:00", "%H:%M").time() <= new_datetime.time() <= datetime.strptime("22:00", "%H:%M").time()):
                return None, "Reservation must be between 12:00 and 22:00."

            new_first_name = form_data.get('first_name')
            new_last_name = form_data.get('last_name')
            new_email = form_data.get('email')
            new_phone = form_data.get('phone')
        except Exception:
            return None, "Invalid input."

        # validation 4: Table capacity check
        table = TableModel.query.get(reservation.table_id)
        if table and new_guest_count > table.seats:
            return None, f"Table {table.table_number} can only seat {table.seats} guests."
        # validation 5: resrvation conflict
        if reservation.reservation_time != new_datetime:
            
            conflict = Reservation.query.filter(
                Reservation.table_id == reservation.table_id,
                Reservation.reservation_time == new_datetime,
                Reservation.id != reservation.id
            ).first()
            
            if conflict:
                return None, "This table is already booked at the selected time."

        # Update reservation fields
        reservation.number_of_people = new_guest_count
        reservation.reservation_time = new_datetime

        # Update customer info
        if reservation.customer:
            reservation.customer.first_name = new_first_name
            reservation.customer.last_name = new_last_name
            reservation.customer.email = new_email
            reservation.customer.phone_number = new_phone

        db.session.commit()
        return reservation, "Reservation and customer updated successfully."
    
    # Delete reservation by ID
    @staticmethod
    def delete_reservation(reservation_id):
        reservation = Reservation.query.get(reservation_id)
        if reservation:
            db.session.delete(reservation)
            db.session.commit()
            return True
        return False
