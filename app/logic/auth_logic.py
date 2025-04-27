from datetime import datetime, timezone


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
    def get_users():
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
    
    @staticmethod
    def get_user_record(username):
        return BaseCRUD.get_row(User, username = username)
    
    @staticmethod
    def get_staff_record(user_id):
        
        return BaseCRUD.get_row(Staff, user_id = user_id)
    

    @staticmethod
    def add_staff(first_name, last_name, phone_number, email, user_id):
        return BaseCRUD.create(
            Staff,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email,
            hire_date = datetime.now(timezone.utc),
            user_id = user_id
        
        )
        
    @staticmethod
    def update_staff(staff_id, first_name, last_name, phone_number, email):
        return BaseCRUD.update(
            Staff,
            staff_id, 
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email,
  
        )
            
            
    @staticmethod
    def change_password(id, new_password):
        return BaseCRUD.update(User, id, password = new_password)
    
    @staticmethod
    def delete_account(user_id):
        staff= BaseCRUD.get_all_records_by_filter(Staff, user_id = user_id)
        if staff:
            staff_id = staff[0].id 
            BaseCRUD.delete(Staff,staff_id)
        BaseCRUD.delete(User, user_id)
        return True
    
    