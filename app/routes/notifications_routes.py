# app/routes/notifications_routes.py
from flask import Blueprint, render_template
from app.logic.notification_logic import NotificationLogic

notifications_bp = Blueprint('notifications', __name__)

@notifications_bp.route('/notifications')
def notifications():
    all_notifications = NotificationLogic.get_all_notifications()
    return render_template('notifications.html', notifications=all_notifications)
