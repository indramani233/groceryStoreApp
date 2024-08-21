from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_security import login_user, current_user, logout_user
from extensions import db

from forms.user_forms import UserSignupForm, StoreManagerSignupForm
from forms.user_forms import LoginForm
from models.user import User

auth_bp = Blueprint('auth', __name__)




@auth_bp.route('/signup/user', methods=['GET', 'POST'])
def user_signup():
    form = UserSignupForm()
    if form.validate_on_submit():
        username = form.username.data
        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash('Username already exists. Please choose a different username.', 'error')
            return render_template('signup.html', form=form)

        user = User(username=username, password=form.password.data, is_store_manager=False)
        db.session.add(user)
        db.session.commit()
        flash('User signed up successfully!', 'success')
        return redirect(url_for('auth.user_login'))
    return render_template('signup.html', form=form)

@auth_bp.route('/signup/store_manager', methods=['GET', 'POST'])
def store_manager_signup():
    form = StoreManagerSignupForm()
    if form.validate_on_submit():
        username = form.username.data
        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash('Username already exists. Please choose a different username.', 'error')
            return render_template('signup.html', form=form)
        user = User(username=form.username.data, password=form.password.data, is_store_manager=True)
        db.session.add(user)
        db.session.commit()
        flash('Approval sent to admin', 'info')
        return redirect(url_for('auth.user_login'))
    return render_template('signup.html', form=form)



@auth_bp.route('/login/user', methods=['GET', 'POST'])
def user_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data, is_store_manager=False).first()
        if user and user.password == form.password.data:
            # Redirect to user dashboard
            return redirect(url_for('user.user_dashboard'))
        else:
            flash('Invalid credentials', 'error')
    return render_template('login.html', form=form)

@auth_bp.route('/login/store_manager', methods=['GET', 'POST'])
def store_manager_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data, is_store_manager=True).first()
        if user and user.password == form.password.data:
            # Check if store manager is approved
            if user.is_approved:
                # Redirect to store manager dashboard
                return redirect(url_for('store_manager.store_manager_dashboard'))
                #return redirect(url_for('store_manager.manage_products'))
            else:
                flash('Your account is pending approval', 'warning')
        else:
            flash('Invalid credentials', 'error')
    return render_template('login.html', form=form)

@auth_bp.route('/login/admin', methods=['GET', 'POST'])
def admin_login():
    form = LoginForm()
    if form.validate_on_submit():
        admin_username = 'admin'  # Predefined admin username
        admin_password = 'adminpassword'  # Predefined admin password
        
        # Check if the entered credentials match the predefined admin credentials
        if form.username.data == admin_username and form.password.data == admin_password:
            # Redirect to admin dashboard upon successful login
            return redirect(url_for('admin.admin_dashboard'))
        else:
            flash('Invalid credentials', 'error')
    return render_template('login.html', form=form)



# @auth_bp.route('/admin/approval')
# def admin_approval():
#     # Fetch pending store manager signups (not yet approved)
#     pending_signups = User.query.filter_by(is_store_manager=True, is_approved=False).all()
#     return render_template('admin_approval.html', pending_signups=pending_signups)


# @auth_bp.route('/admin/approval/<int:user_id>', methods=['POST'])
# def process_approval(user_id):
#     user = User.query.get(user_id)
#     if user:
#         if 'approve' in request.form:
#             user.is_approved = True
#             # Additional logic if needed upon approval
#         elif 'reject' in request.form:
#             # Additional logic if needed upon rejection
#             pass
#         db.session.commit()
#     return redirect(url_for('auth.admin_approval'))
