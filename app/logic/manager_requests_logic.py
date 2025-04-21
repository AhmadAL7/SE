from app.models import RequestTimeOff, Notification
from app import db
from app.logic.base_crud import BaseCRUD
from datetime import datetime

class ManagerRequestLogic(BaseCRUD):

    @staticmethod
    def get_all_requests():
        return BaseCRUD.get_all(RequestTimeOff)

    @staticmethod
    def update_request_status(request_id, new_status):
        request = RequestTimeOff.query.get(request_id)
        if not request:
            return False, "Request not found"

        request.status = new_status
        db.session.commit()

        # Add a notification to manager
        notification = Notification(
            message=f"Request {request.id} has been {new_status.lower()}",
            role="Manager",
            timestamp=datetime.utcnow()
        )
        db.session.add(notification)
        db.session.commit()

        return True, "Status updated"
