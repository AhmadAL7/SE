from flask import Blueprint, render_template, redirect, url_for, request
from app.logic.manager_requests_logic import ManagerRequestLogic

manager_bp = Blueprint('manager', __name__)

@manager_bp.route('/requests')
def requests_manager():
    requests = ManagerRequestLogic.get_all_requests()
    return render_template('requests_manager.html', requests=requests)

@manager_bp.route('/requests/approve/<int:request_id>', methods=['POST'])
def approve_request(request_id):
    success, message = ManagerRequestLogic.update_request_status(request_id, "Approved")
    return redirect(url_for('manager.requests_manager'))

@manager_bp.route('/requests/deny/<int:request_id>', methods=['POST'])
def deny_request(request_id):
    success, message = ManagerRequestLogic.update_request_status(request_id, "Denied")
    return redirect(url_for('manager.requests_manager'))
