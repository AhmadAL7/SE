from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/reservations/create')
def reservations_creation():
    return render_template('reservations_creation.html')

@main.route('/reservations/foh')
def reservations_foh():
    return render_template('reservations_foh.html')

@main.route('/notifications')
def notifications():
    return render_template('notifications.html')

@main.route('/requests/manager')
def requests_manager():
    return render_template('requests_manager.html')
