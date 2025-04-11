from flask import render_template, request, redirect, url_for,Blueprint,flash,session
from app.logic.auth_logic import AuthLogic
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/sign_in', methods=['GET', 'POST'])
#  sign in 
def sign_in():
    # check if user already signed in 
    if 'user_id' in session:
        flash('You are already logged in!', 'info')
        return redirect(url_for('menu.menu')) 
    
    # handle form data
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
 
        # authorize the user's data       
        user = AuthLogic.authorize(username, password)
        if user:
            # add user id and username in the session
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('menu.menu'))
        else:
            flash('Invalid username or password.', 'error')
            return redirect(url_for('auth.sign_in'))
    # view sign in page
    return render_template('sign_in.html')


#sign up 
@auth_bp.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    # form request
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role_id = request.form['role_id']
        encrypted_password =AuthLogic.encrypt_password(password)
        #checck if user exists
        user_exists = AuthLogic.check_user(username)
        if user_exists:
            flash('Username already taken. Please choose another one.', 'error')
            return redirect(url_for('auth.sign_up'))
        # create user
        AuthLogic.create_user( username, password , role_id)
        return redirect(url_for('auth.sign_in'))  
    # get roles for signing up 
    roles = AuthLogic.get_role()
    # view sign up page with roles
    return render_template('sign_up.html',  roles = roles)
