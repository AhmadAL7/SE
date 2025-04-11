from app.models import User, Role, Permission, Staff
from app.logic.base_crud import BaseCRUD
from werkzeug.security import generate_password_hash, check_password_hash

class AuthLogic(BaseCRUD):
    
    @staticmethod
    def create_user(username, password, role_id):
        return BaseCRUD.create(User, username = username, password = password, role_id = role_id)
    @staticmethod
    def encrypt_password(password):
        return generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
    @staticmethod
    def get_role():
        return BaseCRUD.get_all(Role)
    
    @staticmethod
    def get_user():
        return BaseCRUD.get_all(Staff)
    
    @staticmethod
    def authorize(username, password):
        user = BaseCRUD.get_row(User, username = username)
        if user and check_password_hash(user.password, password):
            return user
        return None     
    @staticmethod
    def check_user(username):
        if BaseCRUD.get_row(User, username = username):
            return True
        return None