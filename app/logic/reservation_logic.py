from app.models import Reservation, TableModel, Customer
from app.logic.base_crud import BaseCRUD
from app.logic.reservation_factory import ReservationFactory
from app import db
from datetime import datetime

class ReservationLogic(BaseCRUD):
    def __init__(self):
        pass

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

        # Parse name into first and last
        parts = name.strip().split()
        first_name = parts[0]
        last_name = parts[1] if len(parts) > 1 else ""

        # Match full identity
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

        # ❌ Block if same customer already booked at this time
        existing_booking = Reservation.query.filter_by(
            customer_id=customer.id,
            reservation_time=reservation_datetime
        ).first()
        if existing_booking:
            raise ValueError("You already have a reservation at this time.")

        # ✅ Use the factory to create the reservation instance
        reservation = ReservationFactory.create_reservation(
            customer_id=customer.id,
            reservation_time=reservation_datetime,
            guests=guests
        )

        if not reservation:
            raise ValueError("No available tables for that time and guest count.")

        db.session.add(reservation)
        db.session.commit()
        return reservation

    @staticmethod
    def get_all_reservations():
        return BaseCRUD.get_all(Reservation)

    @staticmethod
    def get_all_reservations_with_customer():
        return db.session.query(Reservation, Customer).join(Customer, Reservation.customer_id == Customer.id).all()

    @staticmethod
    def get_reservation_by_id(reservation_id):
        return BaseCRUD.get_by_id(Reservation, reservation_id)

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

            new_first_name = form_data.get('first_name')
            new_last_name = form_data.get('last_name')
            new_email = form_data.get('email')
            new_phone = form_data.get('phone')
        except Exception:
            return None, "Invalid input."

        table = TableModel.query.get(reservation.table_id)
        if table and new_guest_count > table.seats:
            return None, f"Table {table.table_number} can only seat {table.seats} guests."

        reservation.number_of_people = new_guest_count
        reservation.reservation_time = new_datetime

        if reservation.customer:
            reservation.customer.first_name = new_first_name
            reservation.customer.last_name = new_last_name
            reservation.customer.email = new_email
            reservation.customer.phone_number = new_phone

        db.session.commit()
        return reservation, "Reservation and customer updated successfully."

    @staticmethod
    def delete_reservation(reservation_id):
        reservation = Reservation.query.get(reservation_id)
        if reservation:
            db.session.delete(reservation)
            db.session.commit()
            return True
        return False
