from flask import Blueprint, render_template, redirect, url_for, flash, session
from extensions import db

from models.user import User, Role  # Assuming User model exists
from models.category import Category
from models.product import Product

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/categories', methods=['GET'])
def admin_categories_approval():
    pending_categories = Category.query.filter_by(approval_required=True).all()
    return render_template('admin_dashboard.html', pending_categories=pending_categories)

@admin_bp.route('/admin/categories/approve/<int:category_id>', methods=['POST'])
def approve_category(category_id):
    category = Category.query.get(category_id)
    if category:
        category.approval_required = False  # Approve the category
        db.session.commit()
        # Perform additional actions upon approval if needed
        flash('Category approved!', 'success')
        # Redirect to the admin's categories approval page
        return redirect(url_for('admin.admin_categories_approval'))
    flash('Category approval failed!', 'error')
    return redirect(url_for('admin.admin_categories_approval'))

@admin_bp.route('/admin/categories/reject/<int:category_id>', methods=['POST'])
def reject_category(category_id):
    category = Category.query.get(category_id)
    if category:
        db.session.delete(category)
        db.session.commit()
        # Perform any additional actions upon rejection if needed
        flash('Category rejected!', 'warning')
        # Redirect to the admin's categories approval page
        return redirect(url_for('admin.admin_categories_approval'))
    flash('Category rejection failed!', 'error')
    return redirect(url_for('admin.admin_categories_approval'))
# Other views for adding, editing, removing categories...



@admin_bp.route('/admin_dashboard')
def admin_dashboard():
    # Fetch pending store manager signups (not yet approved)
    pending_signups = User.query.filter_by(is_store_manager=True, is_approved=False).all()

    # Fetch categories waiting for addition or removal
    pending_categories = Category.query.filter_by(approval_required=True).all()

    return render_template('admin_dashboard.html', pending_signups=pending_signups, pending_categories=pending_categories)

@admin_bp.route('/approve/<int:user_id>')
def approve_signup(user_id):
    user = User.query.get(user_id)
    if user:
        user.is_approved = True
        db.session.commit()
        flash('Signup approved successfully!', 'success')
    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/reject/<int:user_id>')
def reject_signup(user_id):
    user = User.query.get(user_id)
    if user:
        # Additional rejection logic if needed
        db.session.delete(user)
        db.session.commit()
        flash('Signup rejected!', 'info')
    return redirect(url_for('admin.admin_dashboard'))



@admin_bp.route('/logout')
def logout():
    # Clear the session for the admin
    session.clear()
    # Redirect to the login page or any other page after logout
    return redirect(url_for('auth.admin_login'))  # Replace 'login' with your login route