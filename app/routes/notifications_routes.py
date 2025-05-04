# app/routes/notifications_routes.py
from flask import Blueprint, redirect, render_template, session, url_for
from app.logic.notification_logic import NotificationLogic
from app.logic.auth_logic import AuthLogic

notifications_bp = Blueprint('notifications', __name__)

# Display staff notifications based on user ID and role
@notifications_bp.route('/notifications')
def notifications():
    user_id = session.get('user_id')
    role_id = session.get('role_id')
# Redirect if not logged in
    if not user_id or not role_id:
        return redirect(url_for('auth.sign_in'))

        # Retrieve staff and role data
    staff = AuthLogic.get_staff_record(user_id)
    role = NotificationLogic.get_role(role_id)

    if not staff or not role:
        return "No access to notifications."
  # Get  notifications (staff or role based)
    notifications = NotificationLogic.get_notifications_for_staff_and_role(
        staff.id,
        role.role_name
    )

    return render_template('notifications.html', notifications=notifications)
