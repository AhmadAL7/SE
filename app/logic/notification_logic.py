# app/logic/notification_logic.py
from app.models import Notification
from app.logic.base_crud import BaseCRUD

class NotificationLogic(BaseCRUD):
    def __init__(self):
        pass

    @staticmethod
    def get_all_notifications():
        return BaseCRUD.get_all(Notification)
