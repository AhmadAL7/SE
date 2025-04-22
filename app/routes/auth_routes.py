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
        AuthLogic.create_user( username, encrypted_password , role_id)
        return redirect(url_for('auth.sign_in'))  
    # get roles for signing up 
    roles = AuthLogic.get_role()
    # view sign up page with roles
    return render_template('sign_up.html',  roles = roles)

#profile
@auth_bp.route('/profile', methods=['GET', 'POST'])
def get_profile():
    username = session.get('username')
    user_id = session.get('user_id')
    user = AuthLogic.get_user_record(username)
    staff_data = user.staff  # using relationship in models
    if request.method == 'POST':
        # if staff exists
        if staff_data:
            new_password = request.form['password']
            if new_password:
                encrypted_password =AuthLogic.encrypt_password(new_password)
                AuthLogic.change_password(user_id, encrypted_password)
            AuthLogic.update_staff(
                staff_id=staff_data.id,
                first_name=request.form['first_name'],
                last_name=request.form['last_name'],
                phone_number=request.form['phone_number'],
                email=request.form['email']
            )
            return redirect(url_for('auth.get_profile'))
        # add record for staff
        AuthLogic.add_staff(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        phone_number=request.form['phone_number'],
        email=request.form['email'],
        user_id = user_id
        )  

 
    return render_template('profile.html',  user_data=user, staff_data=staff_data)

@auth_bp.route('/delete_account', methods=['POST'])
def delete_account():
    username = session.get('username')
    
    # If user is logged in
    if username:
        user_id = AuthLogic.get_user_record(username).id
        
        # Only delete if user exists
        if user_id:
            AuthLogic.delete_account(user_id)
            session.clear()
            
            return redirect(url_for('auth.sign_in'))
        
        else:
            print("User not found. Unable to delete account.", "error")
            return redirect(url_for('auth.get_profile'))

    # If user is somehow not logged in
    print("user not in session")
    return redirect(url_for('auth.get_profile'))
# logout 
@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('auth.sign_in'))