from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.logic.support_logic import SupportLogic

support_bp = Blueprint('support', __name__)

@support_bp.route('/support', methods=['GET', 'POST'])
def support_page():
    if request.method == 'POST':
        email = request.form.get('email')
        inquiry_text = request.form.get('inquiry_text')

        try:
            SupportLogic.create_support(email, inquiry_text)
            return render_template('support_form.html', success="Your message has been sent!")
        except ValueError as e:
            return render_template('support_form.html', error=str(e))

    return render_template('support_form.html')

@support_bp.route('/manager/queries')
def view_queries():
    supports = SupportLogic.get_all_supports()
    return render_template('manager_queries.html', supports=supports)
