from flask import Blueprint, redirect, url_for, flash, request
from app import db
from models.product import Product

update_inventory_bp = Blueprint('update_inventory', __name__)

@update_inventory_bp.route('/update_inventory/<int:product_id>', methods=['POST'])
def update_inventory(product_id):
    # ... existing logic ...
    # Fetch the product
    product = Product.query.get(product_id)

    if not product:
        flash('Product not found!', 'error')
        return redirect(url_for('user.user_dashboard'))

    new_quantity = int(request.form.get('new_quantity'))

    if new_quantity < 0:
        flash('Invalid quantity!', 'error')
        return redirect(url_for('user.user_dashboard'))

    product.quantity_available = new_quantity
    db.session.commit()

    flash('Inventory updated successfully!', 'success')
    return redirect(url_for('user.user_dashboard'))
    
