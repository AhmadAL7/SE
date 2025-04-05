from flask import Blueprint, render_template

# Create a blueprint for reservations routes
reservations_bp = Blueprint('reservations', __name__)

@reservations_bp.route('/reservations/create')
def reservations_creation():
    return render_template('reservations_creation.html')

@reservations_bp.route('/reservations/foh')
def reservations_foh():
    return render_template('reservations_foh.html')
