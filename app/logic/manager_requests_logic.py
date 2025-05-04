from app.models import RequestTimeOff, Notification
from app import db
from app.logic.base_crud import BaseCRUD
from datetime import datetime, timezone

class ManagerRequestLogic(BaseCRUD):
    
   # Get all pending time-off requests
    @staticmethod
    def get_pending_requests():
        return RequestTimeOff.query.filter_by(status='Pending').all()
    
# Approve or reject a request and notify staff
    @staticmethod
    def update_request_status(request_id, new_status):
        request = RequestTimeOff.query.get(request_id)
        if not request:
            return False, "Request not found"

        request.status = new_status
        db.session.commit()

        # Get staff who submitted the request
        staff = request.staff  # uses backref='staff' in RequestTimeOff model
        user = staff.user if staff else None
        role_name = user.role.role_name if user and user.role else "Unknown"

        # Create notification for the requester
        notification = Notification(
            message=f"Your time off request #{request.id} has been {new_status.lower()}",
            role=role_name,                     
            staff_id=staff.id,                  
            timestamp=datetime.now(timezone.utc)
        )

        db.session.add(notification)
        db.session.commit()

        return True, "Status updated"
    
# Submit a new time-off request
    @staticmethod
    def create_time_off_request(form_data, staff_id):
        new_request = RequestTimeOff(
            staff_id=staff_id,
            reason=form_data.get("reason"),
            request_start=datetime.strptime(form_data.get("start_date"), "%Y-%m-%d"),
            request_end=datetime.strptime(form_data.get("end_date"), "%Y-%m-%d"),
            status="Pending"
        )
        db.session.add(new_request)
        db.session.commit()
