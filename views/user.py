from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from extensions import db

from models.category import Category
from models.product import Product

user_bp = Blueprint('user', __name__)

@user_bp.route('/user_dashboard', methods=['GET', 'POST'])
def user_dashboard():
    categories = Category.query.all()
    search_results = []

    if request.method == 'GET':
        search_query = request.args.get('search_query')
        category_filter = request.args.get('category')

        if search_query or category_filter:
            # Implement search logic based on filters
            if search_query:
                search_results = Product.query.filter(Product.name.ilike(f'%{search_query}%')).all()
            elif category_filter:
                search_results = Product.query.filter_by(category_id=category_filter).all()

    return render_template('user_dashboard.html', categories=categories, search_results=search_results)

@user_bp.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    product = Product.query.get(product_id)
    if not product:
        flash('Product not found!', 'error')
        return redirect(url_for('user.user_dashboard'))

    quantity = int(request.form.get('quantity'))
    if quantity <= 0:
        flash('Invalid quantity!', 'error')
        return redirect(url_for('user.user_dashboard'))

    if product.quantity_available < quantity:
        flash('Insufficient quantity!', 'error')
        return redirect(url_for('user.user_dashboard'))
    # Logic to add product to cart
    # For example, using sessions
    cart = session.get('cart', {})
    cart_item = {
        'product_id': product.id,
        'name': product.title,
        'quantity': quantity,
        'cost': product.cost * quantity
    }
    cart[product.id] = cart_item
    session['cart'] = cart

    flash('Product added to cart!', 'success')
    return redirect(url_for('user.user_dashboard'))


@user_bp.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    if product_id in cart:
        cart.pop(product_id)
        session['cart'] = cart
        flash('Item removed from cart!', 'success')
    return redirect(url_for('user.view_cart'))


@user_bp.route('/view_cart', methods=['GET'])
def view_cart():
    cart = session.get('cart', {})
    return render_template('view_cart.html', cart=cart)

@user_bp.route('/checkout', methods=['POST'])
def checkout():
    cart = session.get('cart', {})
    for item_id, item in cart.items():
        product = Product.query.get(item['product_id'])
        if not product or product.quantity_available < item['quantity']:
            flash(f'Error: Item {item["name"]} not available in sufficient quantity!', 'error')
            return redirect(url_for('user.view_cart'))

    # Process checkout
    # ... (Order processing logic)

    # Update inventory after successful checkout
    for item_id, item in cart.items():
        product = Product.query.get(item['product_id'])
        product.quantity_available -= item['quantity']
        db.session.commit()

    session.pop('cart', None)
    flash('Order placed successfully!', 'success')
    return redirect(url_for('user.user_dashboard'))

@user_bp.route('/logout')
def logout():
    session.clear()  # Clear the session for the user
    return redirect(url_for('auth.user_login'))  # Redirect to the login page