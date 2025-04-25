from app.logic.base_crud import BaseCRUD
from app.models import Staff, StaffSchedule

class Schedule(BaseCRUD):
    
    
    @staticmethod
    def CreateSchedule(staff_id, shift_start, shift_end):
         BaseCRUD.create(StaffSchedule, staff_id = staff_id, shift_start = shift_start, shift_end = shift_end)
         return True
     
    @staticmethod
    def get_staff():
        return BaseCRUD.get_all(Staff)
    
    @staticmethod
    def get_staff_by_user_id(user_id):
        return BaseCRUD.get_all_records_by_filter(Staff, user_id = user_id)
    
    @staticmethod
    def get_schedule(staff_id, start, end):
        return BaseCRUD.get_records_by_date_range(StaffSchedule,StaffSchedule.shift_start,start_date = start, end_date = end, staff_id = staff_id )
    
    @staticmethod
    def delete_schedule(schedule_id):
        return BaseCRUD.delete(StaffSchedule, schedule_id)
