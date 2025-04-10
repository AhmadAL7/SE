# app/logic/reservation_logic.py

class ReservationLogic:
    @staticmethod
    def create_reservation(form_data):
        name = form_data.get('name')
        date = form_data.get('date')
        time = form_data.get('time')
        guests = form_data.get('guests')

        # Placeholder: for now, just log the data
        print(f"[LOGIC] New Reservation Submitted:")
        print(f"Name: {name}, Date: {date}, Time: {time}, Guests: {guests}")

        # Later, integrate this with your shared DB base class
