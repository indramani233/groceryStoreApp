from flask import Blueprint, session, redirect, url_for
from app import db
from models.product import Product

buy_bp = Blueprint('buy', __name__)

@buy_bp.route('/buy/<int:product_id>')
def buy_product(product_id):
    # Logic to buy a product and add it to the cart

    product = Product.query.get(product_id)
    if product:
        cart = session.get('cart', [])
        cart.append(product_id)
        session['cart'] = cart
        return redirect(url_for('cart.view_cart'))
    else:
        # Handle product not found scenario, redirect to an error page or return an error message
        pass
