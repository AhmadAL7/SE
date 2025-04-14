# app/routes/manager_routes.py
from flask import render_template, Blueprint
from app.logic.manager_requests_logic import ManagerRequestLogic

manager_bp = Blueprint('manager', __name__)

@manager_bp.route('/requests/manager')
def requests_manager():
    requests = ManagerRequestLogic.get_all_requests()
    return render_template('requests_manager.html', requests=requests)
