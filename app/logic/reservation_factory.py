from app.models import Reservation, TableModel

class ReservationFactory:
    @staticmethod
    def create_reservation(customer_id, reservation_time, guests):
        suitable_tables = TableModel.query.filter(TableModel.seats >= guests).all()
        for table in suitable_tables:
            conflict = Reservation.query.filter_by(
                reservation_time=reservation_time,
                table_id=table.id
            ).first()
            if not conflict:
                return Reservation(
                    customer_id=customer_id,
                    reservation_time=reservation_time,
                    number_of_people=guests,
                    table_id=table.id
                )
        return None
