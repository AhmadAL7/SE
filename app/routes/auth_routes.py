from datetime import datetime
from flask import render_template, request, redirect, url_for,Blueprint,flash,session
from app.logic.auth_logic import AuthLogic
from app.logic.schedules import Schedule
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/sign_in', methods=['GET', 'POST'])
#  sign in 
def sign_in():
    


    
    # handle form data
    if request.method == 'POST':
            # check if user already signed in 
        if 'user_id' in session:
            flash('You are already logged in!', 'signin_info')
            return redirect(url_for('auth.sign_in')) 
        
        username = request.form['username']
        password = request.form['password']
        
            # IP address check to allow only in restaurant login and prevent fake clock ins
        ip_address = request.remote_addr
        if not ip_address.startswith('1'): #can specified for deployment
            flash("Login only allowed inside the restaurant network.", "signin_error")
            return redirect(url_for('auth.sign_in'))
            
        # authorize the user's data       
        user = AuthLogic.authorize(username, password)
        if user:
            # add user id and username in the session
            session['user_id'] = user.id   
            session['username'] = user.username
            session['role_id'] = user.role_id
            session['role_name'] = user.role.role_name
            
            # Check if this user is a Staff to initiate clock in
            staff = Schedule.get_staff_record(user_id=user.id)
            if staff:
                clock_in_record = Schedule.clock_in(staff.id)
                session['clock_in_id'] = clock_in_record.id
            
            flash('Login successful!', 'auth_info')
            return redirect(url_for('menu.menu'))
        else:
            flash('Invalid username or password.', 'signin_error')
            return redirect(url_for('auth.sign_in'))
    # view sign in page
    return render_template('sign_in.html')


#sign up 
@auth_bp.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    

    
    # form request
    if request.method == 'POST':
        
        # IP address check to allow only in restaurant login and prevent fake clock ins
        ip_address = request.remote_addr
        if not ip_address.startswith('1'): #can specified for deployment
            flash("sign up only allowed inside the restaurant network.", "signup_error")
            return redirect(url_for('auth.sign_in'))
    
        if 'user_id' not in session: 
                flash("Manager needs to login", "signup_error")
                return redirect(url_for('auth.sign_in'))
        elif session.get('role_name') != 'Management':
                flash("Only mangers can acccess this feature", "signup_error")
                return redirect(url_for('auth.sign_in'))
        # get form data    
        username = request.form['username']
        password = request.form['password']
        role_id = request.form['role_id']
        encrypted_password =AuthLogic.encrypt_password(password)
        #checck if user exists
        user_exists = AuthLogic.check_user(username)
        if user_exists:
            flash('Username already taken. Please choose another one.', 'signup_error')
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
    staff = user.staff  # using relationship in models
    hours = None
    if request.method == 'POST':
            # if staff exists, update
            if staff:
                new_password = request.form['password']
                if new_password:
                    encrypted_password =AuthLogic.encrypt_password(new_password)
                    AuthLogic.change_password(user_id, encrypted_password)
                AuthLogic.update_staff(
                    staff_id=staff.id,
                    first_name=request.form['first_name'],
                    last_name=request.form['last_name'],
                    phone_number=request.form['phone_number'],
                    email=request.form['email']
                )
                return redirect(url_for('auth.get_profile'))
            else:
                # add record for staff
                AuthLogic.add_staff(
                first_name=request.form['first_name'],
                last_name=request.form['last_name'],
                phone_number=request.form['phone_number'],
                email=request.form['email'],
                user_id = user_id)  
                
                return redirect(url_for('auth.get_profile'))
    else: #  handle tracking hours
        start = request.args.get('start')
        end = request.args.get('end')
        
        if start and end:
            try:
                start_date = datetime.fromisoformat(start)
                end_date = datetime.fromisoformat(end)
                hours = Schedule.get_worked_hours_in_range(staff.id, start_date, end_date)
                
            except ValueError:
                flash("Invalid date format.", "profile_error")
                return redirect(url_for('auth.get_profile'))

    return render_template('profile.html', hours=hours, user_data = user, staff_data = staff)



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
            flash("You are not logged in.", "profile_error")
            return redirect(url_for('auth.get_profile'))

    # If user is somehow not logged in
    return redirect(url_for('auth.get_profile'))
# logout 
@auth_bp.route('/logout')
def logout():
    username = session.get('username')

    user = AuthLogic.get_user_record(username)
    if user:
        # Check if this user is a Staff to initiate clock out
        staff = Schedule.get_staff_record(user_id=user.id)
        if staff:
            try:
               Schedule.clock_out(staff.id)
            except ValueError as e:
                flash("No clock_in record found", "logout_error")
    session.clear()
    flash("You have been logged out.", "logout_info")
    return redirect(url_for('auth.sign_in'))


#tracking hours
@auth_bp.route('/profile/tracking')
def get_hours():
    username = session.get('username')
    if not username:
        return redirect(url_for('auth.sign_in'))
    user = AuthLogic.get_user_record(username)
    staff = user.staff
    hours = 0;
    
    
    if staff: 
        staff_id = staff.id
        start_str = request.args.get('start')
        end_str = request.args.get('end')

        try: # ensure format is correct
            start = datetime.fromisoformat(start_str) if start_str else None
            end = datetime.fromisoformat(end_str) if end_str else None
            hours = Schedule.get_worked_hours_in_range(staff_id, start, end)
        except ValueError:
            return redirect(url_for('auth.get_profile'))
        
        
        
        
    return render_template('profile.html', hours=hours, user_data = user, staff_data = staff)