

import unittest
from datetime import datetime, timedelta
from app import create_app, db
from app.models import Customer, Reservation, TableModel, ReminderLog
from app.logic.reservation_remind import Reservation_reminders
from app.logic.base_crud import BaseCRUD
from tests.test_config import TestConfig

class DummyReservationTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_dummy_reservation_flow(self):
        now = datetime.now()

        # Create dummy table
        table = BaseCRUD.create(TableModel, table_number=9999, seats=4)

        # Create dummy customer
        customer = BaseCRUD.create(
            Customer,
            first_name="Dummy",
            last_name="Tester",
            email="dummytester@example.com",
            phone_number="123456789"
        )

        # Create dummy reservation
        reservation_time = now + timedelta(hours=23, minutes=45)
        reservation = BaseCRUD.create(
            Reservation,
            customer_id=customer.id,
            reservation_time=reservation_time,
            number_of_people=2,
            table_id=table.id
        )

        # Send reminders
        Reservation_reminders.send_reminders()

        # Check ReminderLog
        reminder = BaseCRUD.get_row(ReminderLog, customer_id=customer.id, reservation_id=reservation.id)

        self.assertIsNotNone(reminder, "ReminderLog was not created.")

if __name__ == '__main__':
    unittest.main()
