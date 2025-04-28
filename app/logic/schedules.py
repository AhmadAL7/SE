from datetime import datetime, timezone
from app.logic.base_crud import BaseCRUD
from app.models import Staff, StaffSchedule, ClockInOut

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
    
    @staticmethod
    def clock_in(staff_id):
        if not staff_id:
            raise ValueError("Staff ID is required for clock-in.")
        now = datetime.now(timezone.utc)
        return BaseCRUD.create(ClockInOut, staff_id = staff_id, clock_in_time = now)

    @staticmethod
    def clock_out(staff_id):
        if not staff_id:
            raise ValueError("Staff ID is required for clock-out.")
        
        clock_in_record = BaseCRUD.get_first_record_by_filter(ClockInOut, staff_id = staff_id, clock_out_time=None)
        if not clock_in_record:
            raise ValueError("No active clock-in record found.")
        
        now = datetime.now()
        duration = now - clock_in_record.clock_in_time
        
        return Schedule.update(
            ClockInOut,
            clock_in_record.id,
            clock_out_time=now,
            total_hours=round(duration.total_seconds(), 2) # add /3600 for hours in deploymenet
        )
        
    @staticmethod
    def get_worked_hours_in_range(staff_id, start_date, end_date):
        records = BaseCRUD.get_records_by_date_range(
            ClockInOut,
            ClockInOut.clock_in_time,
            start_date=start_date,
            end_date=end_date,
            staff_id=staff_id
        )
        
        total_hours = sum(record.total_hours or 0 for record in records) # OR 0  TO HANDLE NONE VALUE
        return round(total_hours, 2)    
    
    @staticmethod
    def get_staff_record(user_id):
        return BaseCRUD.get_first_record_by_filter(Staff, user_id = user_id)