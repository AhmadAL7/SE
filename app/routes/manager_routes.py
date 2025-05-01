from flask import Blueprint, render_template, redirect, session, url_for, request
from app.logic.Inventory import InventoryLogic
from app.logic.manager_requests_logic import ManagerRequestLogic
from datetime import datetime
from app.models import Staff, StaffSchedule
from app.logic.schedules import Schedule
from app.logic.auth_logic import AuthLogic

import csv
from app.logic.reservation_remind import Reservation_reminders
from flask import Response

manager_bp = Blueprint('manager', __name__)

# View all pending manager requests
@manager_bp.route('/requests')
def requests_manager():
    requests = ManagerRequestLogic.get_pending_requests()
    return render_template('requests_manager.html', requests=requests)

# Approve a request
@manager_bp.route('/requests/approve/<int:request_id>', methods=['POST'])
def approve_request(request_id):
    ManagerRequestLogic.update_request_status(request_id, "Approved")
    return redirect(url_for('manager.requests_manager'))

# Deny a request
@manager_bp.route('/requests/deny/<int:request_id>', methods=['POST'])
def deny_request(request_id):
    ManagerRequestLogic.update_request_status(request_id, "Denied")
    return redirect(url_for('manager.requests_manager'))

# Create new time off request
@manager_bp.route('/requests/create', methods=['GET', 'POST'])
def create_request():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.sign_in'))

    if request.method == 'POST':
        staff = AuthLogic.get_staff_record(user_id)
        if not staff:
            return "You're not registered as staff."
        ManagerRequestLogic.create_time_off_request(request.form, staff.id)
        return redirect(url_for('manager.requests_manager'))

    return render_template('request_create.html')


#  Trigger reminders manually from dashboard
@manager_bp.route('/send_reminders', methods=['POST'])
def trigger_reminders():
    Reservation_reminders.send_reminders()
    return redirect(url_for('manager.requests_manager'))

# Schedule creation
@manager_bp.route('/schedule', methods=['GET', 'POST'])
def create_schedule():
    if request.method == 'POST':
        staff_id = request.form['staff_id']
        shift_start = datetime.fromisoformat(request.form['shift_start'])
        shift_end = datetime.fromisoformat(request.form['shift_end'])
        Schedule.CreateSchedule(staff_id, shift_start, shift_end)
        return redirect(url_for('manager.create_schedule'))

    staff = Schedule.get_staff()
    return render_template('schedule_creation.html', staff_members=staff)

@manager_bp.route('/view_schedule')
def get_my_schedule():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.sign_in'))

    staff_id = Schedule.get_staff_by_user_id(user_id)[0].id
    start_str = request.args.get('start')
    end_str = request.args.get('end')

    try:
        start = datetime.fromisoformat(start_str) if start_str else None
        end = datetime.fromisoformat(end_str) if end_str else None
    except ValueError:
        return "Invalid date format."

    schedules = Schedule.get_schedule(staff_id, start, end)
    return render_template('view_schedule.html', schedules=schedules)

@manager_bp.route('/manage_schedule')
def view_staff_schedules():
    staff = Schedule.get_staff()
    staff_id = request.args.get('staff_id')
    start_str = request.args.get('start')
    end_str = request.args.get('end')

    schedules = []
    if staff_id:
        try:
            start = datetime.fromisoformat(start_str) if start_str else None
            end = datetime.fromisoformat(end_str) if end_str else None
        except ValueError:
            return redirect(url_for('manager.view_staff_schedules'))

        schedules = Schedule.get_schedule(staff_id, start, end)

    return render_template('manage_schedules.html', staff_members=staff, schedules=schedules)

@manager_bp.route('/delete_schedule/<int:schedule_id>', methods=['POST'])
def delete_schedule(schedule_id):
    Schedule.delete_schedule(schedule_id)
    return redirect(url_for('manager.view_staff_schedules'))


# Reports page
@manager_bp.route('/reports')
def manager_reports():
    inventory_usage = InventoryLogic.get_all_inventory_items()
    low_stock_items = InventoryLogic.get_low_stock_items(threshold=5)
    return render_template('reports.html', inventory_usage=inventory_usage, low_stock_items=low_stock_items)


@manager_bp.route('/download_inventory_usage_csv')
def download_inventory_usage_csv():
    inventory_items = InventoryLogic.get_all_inventory_items()

    # Prepare CSV output
    def generate():
        data = [["Item Name", "Quantity", "Used Quantity"]]
        for item in inventory_items:
            data.append([item.item_name, item.quantity, item.used_quantity])

        # Convert to CSV format
        for row in data:
            yield  ','.join(map(str, row)) + '\n' # turn into string each item in a row then join them (add new line between rows)

    #  response to retun the csv file , tell the browser to download not shoe, set name
    return Response(generate(), mimetype='text/csv',
                    headers={"Content-Disposition": "attachment;filename=inventory_usage_report.csv"})

@manager_bp.route('/download_low_inventory_csv')
def download_low_inventory_csv():
    low_inventory_items = InventoryLogic.get_low_stock_items()
    def generate():
         data = [["Item Name", "Quantity", "Supplier"]]
         for  item in low_inventory_items:
              data.append([item.item_name, item.quantity, item.supplier.name])
              
         for row in data:
             yield  ','.join(map(str,row)) + '\n' 
         
    
    return Response(generate(), mimetype='text/csv', headers = {"Content-disposition": "attachment;filename=low_inventory_report.csv"})