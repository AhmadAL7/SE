# app/logic/notification_logic.py
from app.models import Notification, Role
from app.logic.base_crud import BaseCRUD

class NotificationLogic(BaseCRUD):
    def __init__(self):
        pass
# Get notifications for specific staff or their role
    @staticmethod
    def get_notifications_for_staff_and_role(staff_id, role_name):

        return BaseCRUD.get_staff_sensitive_notifications(Notification, staff_id, role_name)
    # Get role by ID
    @staticmethod
    def get_role(role_id):
        return BaseCRUD.get_by_id(Role, role_id)