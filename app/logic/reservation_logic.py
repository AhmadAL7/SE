# app/logic/reservation_logic.py

from app.models import Reservation, TableModel, Customer
from app.logic.base_crud import BaseCRUD
from app import db
from datetime import datetime

class ReservationLogic(BaseCRUD):
    def __init__(self):
        pass

    @staticmethod
    def create_reservation(form_data):
        name = form_data.get('name')
        date = form_data.get('date')
        time = form_data.get('time')
        guests = form_data.get('guests')

        print(f"[LOGIC] New Reservation Submitted:")
        print(f"Name: {name}, Date: {date}, Time: {time}, Guests: {guests}")

        reservation_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
        dummy_customer_id = 1
        dummy_table_id = 1

        return BaseCRUD.create(
            Reservation,
            customer_id=dummy_customer_id,
            reservation_time=reservation_datetime,
            number_of_people=guests,
            table_id=dummy_table_id
        )

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

        new_guest_count = int(form_data.get('guests'))
        new_name = form_data.get('name')  # Placeholder, not stored yet

        table = TableModel.query.get(reservation.table_id)
        if table and new_guest_count > table.seats:
            return None, f"Table {table.table_number} can only seat {table.seats} guests."

        reservation.number_of_people = new_guest_count
        db.session.commit()
        return reservation, "Reservation updated successfully."

    @staticmethod
    def delete_reservation(reservation_id):
        reservation = Reservation.query.get(reservation_id)
        if reservation:
            db.session.delete(reservation)
            db.session.commit()
            return True
        return False
