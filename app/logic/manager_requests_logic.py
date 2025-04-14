# app/logic/manager_requests_logic.py
from app.models import RequestTimeOff
from app.logic.base_crud import BaseCRUD

class ManagerRequestLogic(BaseCRUD):
    @staticmethod
    def get_all_requests():
        return BaseCRUD.get_all(RequestTimeOff)
