# tests/test_reservation_factory.py

import unittest
from datetime import datetime
from app import create_app, db
from app.models import Customer, TableModel
from app.logic.reservation_factory import ReservationFactory
from tests.test_config import TestConfig

class ReservationFactoryTestCase(unittest.TestCase):
    def setUp(self):
        # Pass test config into app factory
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Add dummy data
        self.customer = Customer(first_name="Test", last_name="User", email="test@example.com", phone_number="1234567890")
        self.table = TableModel(table_number=101, seats=4)

        db.session.add_all([self.customer, self.table])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_reservation_created_successfully(self):
        reservation_time = datetime(2025, 5, 10, 18, 0)
        reservation = ReservationFactory.create_reservation(
            customer_id=self.customer.id,
            reservation_time=reservation_time,
            guests=2
        )

        self.assertIsNotNone(reservation)
        self.assertEqual(reservation.customer_id, self.customer.id)
        self.assertEqual(reservation.number_of_people, 2)

if __name__ == '__main__':
    unittest.main()
