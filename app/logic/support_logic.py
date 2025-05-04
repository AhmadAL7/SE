from datetime import datetime

from app.logic.base_crud import BaseCRUD
from app.models import Support


class SupportLogic(BaseCRUD):
    # Create new support ticket
    @staticmethod
    def create_support(email, inquiry_text):
        if not email or not inquiry_text:
            raise ValueError("Email and inquiry text are required.")

        return SupportLogic.create(
            Support,
            email=email,
            inquiry_date=datetime.now(),
            inquiry_text=inquiry_text
        )
        
    # Get all support tickets
    @staticmethod
    def get_all_supports():
        return BaseCRUD.get_all(Support)    