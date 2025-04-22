from app.models import RequestTimeOff, Notification
from app import db
from app.logic.base_crud import BaseCRUD
from datetime import datetime

class ManagerRequestLogic(BaseCRUD):

    @staticmethod
    def get_pending_requests():
        return RequestTimeOff.query.filter_by(status='Pending').all()

    @staticmethod
    def update_request_status(request_id, new_status):
        request = RequestTimeOff.query.get(request_id)
        if not request:
            return False, "Request not found"

        request.status = new_status
        db.session.commit()

        # Add a notification
        notification = Notification(
            message=f"Request {request.id} has been {new_status.lower()}",
            role="Manager",
            timestamp=datetime.utcnow()
        )
        db.session.add(notification)
        db.session.commit()

        return True, "Status updated"

    @staticmethod
    def create_time_off_request(form_data):
        new_request = RequestTimeOff(
            staff_id=form_data.get("staff_id"),
            reason=form_data.get("reason"),
            request_start=datetime.strptime(form_data.get("start_date"), "%Y-%m-%d"),
            request_end=datetime.strptime(form_data.get("end_date"), "%Y-%m-%d"),
            status="Pending"
        )
        db.session.add(new_request)
        db.session.commit()
