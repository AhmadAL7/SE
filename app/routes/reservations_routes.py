# app/routes/reservations_routes.py

from flask import Blueprint, render_template, request
from app.logic.reservation_logic import ReservationLogic

# Create a blueprint for reservations routes
reservations_bp = Blueprint('reservations', __name__)

@reservations_bp.route('/reservations/create', methods=['GET', 'POST'])
def reservations_creation():
    if request.method == 'POST':
        # Delegate form processing to logic class
        ReservationLogic.create_reservation(request.form)
        return render_template('reservations_creation.html', message="Reservation submitted!")

    return render_template('reservations_creation.html')


@reservations_bp.route('/reservations/foh')
def reservations_foh():
    return render_template('reservations_foh.html')
