import pytest
from app import create_app, db
from app.models import TableModel, Order
from tests.test_config import TestConfig  # import your TestConfig!

@pytest.fixture
def client():
    app = create_app(TestConfig)
    with app.test_client() as client:  # create tesiing client
        with app.app_context():
            db.create_all()
            
            # Setup dummy data
            table = TableModel(table_number=1010, seats=4)
            db.session.add(table)
            db.session.commit()

            order = Order(
                order_date='2025-04-28 12:00:00',
                table_id=table.id,
                status='Pending',
                total_price=50.0,
                payment_status='Unpaid'
            )
            db.session.add(order)
            db.session.commit()

        yield client # give client to test funtion
        # CLEANUP 
        with app.app_context():
            db.session.remove()
            db.drop_all()

def test_fake_payment_success(client):
    # Post payment for table_id=1
    response = client.post('/pay/1010', data={'amount': 60.0}, follow_redirects=True)

    assert response.status_code == 200 # ensure page is return 
    assert b'Payment' in response.data or b'Table' in response.data

    # Check if payment status updated
    order = Order.query.first()
    assert order.payment_status == 'Paid'
    
    # after running test it clean db  auto
