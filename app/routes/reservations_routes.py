from flask import Blueprint, render_template, request, redirect, url_for
from app.logic.reservation_logic import ReservationLogic

reservations_bp = Blueprint('reservations', __name__)
# Create a new reservation
@reservations_bp.route('/reservations/create', methods=['GET', 'POST'])
def reservations_creation():
    if request.method == 'POST':
        try:
            ReservationLogic.create_reservation(request.form)
            return render_template('reservations_creation.html', message="Reservation booked successfully!")
        except ValueError as e:
            return render_template('reservations_creation.html', error=str(e))
    return render_template('reservations_creation.html')
# View all reservations 
@reservations_bp.route('/reservations/foh')
def reservations_foh():
    reservations = ReservationLogic.get_all_reservations_with_customer()
    return render_template('reservations_foh.html', 
                           reservations=reservations)


# Edit an existing reservation by ID
@reservations_bp.route('/reservations/edit/<int:id>', methods=['GET', 'POST'])
def edit_reservation(id):
    reservation = ReservationLogic.get_reservation_by_id(id)
    if not reservation:
        return "Reservation not found", 404

    if request.method == 'POST':
        updated_reservation, message = ReservationLogic.update_reservation_with_validation(id, request.form)
        if updated_reservation:
            return render_template('reservations_edit.html', 
                                   reservation=updated_reservation, 
                                   message=message)
        else:
            return render_template('reservations_edit.html', 
                                   reservation=reservation, 
                                   error=message)

    return render_template('reservations_edit.html', 
                           reservation=reservation)
# Cancel a reservation by ID
@reservations_bp.route('/reservations/cancel/<int:id>', methods=['POST'])
def cancel_reservation(id):
    deleted = ReservationLogic.delete_reservation(id)
    if deleted:
        return redirect(url_for('reservations.reservations_foh'))
    else:
        return "Reservation not found", 404
