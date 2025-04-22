from flask import Blueprint, render_template, redirect, url_for, request
from app.logic.manager_requests_logic import ManagerRequestLogic

manager_bp = Blueprint('manager', __name__)

# View all pending manager requests
@manager_bp.route('/requests')
def requests_manager():
    requests = ManagerRequestLogic.get_pending_requests()  # Only show pending ones
    return render_template('requests_manager.html', requests=requests)

# Approve a specific request
@manager_bp.route('/requests/approve/<int:request_id>', methods=['POST'])
def approve_request(request_id):
    ManagerRequestLogic.update_request_status(request_id, "Approved")
    return redirect(url_for('manager.requests_manager'))

# Deny a specific request
@manager_bp.route('/requests/deny/<int:request_id>', methods=['POST'])
def deny_request(request_id):
    ManagerRequestLogic.update_request_status(request_id, "Denied")
    return redirect(url_for('manager.requests_manager'))

# Create a new time off request
@manager_bp.route('/requests/create', methods=['GET', 'POST'])
def create_request():
    if request.method == 'POST':
        ManagerRequestLogic.create_time_off_request(request.form)
        return redirect(url_for('manager.requests_manager'))
    return render_template('request_create.html')
