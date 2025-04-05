from flask import Blueprint, render_template

# Create a blueprint for notifications routes
notifications_bp = Blueprint('notifications', __name__)

@notifications_bp.route('/notifications')
def notifications():
    return render_template('notifications.html')
