# app/logic/reservation_logic.py
from app.models import Reservation
from app.logic.base_crud import BaseCRUD
from datetime import datetime

class ReservationLogic(BaseCRUD):
    def __init__(self):
        pass

    @staticmethod
    def create_reservation(form_data):
        name = form_data.get('name')  # Optional for logging or future use
        date = form_data.get('date')
        time = form_data.get('time')
        guests = form_data.get('guests')

        print(f"[LOGIC] New Reservation Submitted:")
        print(f"Name: {name}, Date: {date}, Time: {time}, Guests: {guests}")

        # Combine date and time into a single datetime object
        reservation_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")

        # Temporary hardcoded values for customer_id and table_id until user selection is implemented
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