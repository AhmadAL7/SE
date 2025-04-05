from flask import Blueprint, render_template

# Create a blueprint for manager-related routes
manager_bp = Blueprint('manager', __name__)

@manager_bp.route('/requests/manager')
def requests_manager():
    return render_template('requests_manager.html')
