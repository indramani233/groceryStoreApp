from flask import Blueprint, render_template, request
from app import db
from models.product import Product

search_bp = Blueprint('search', __name__)

@search_bp.route('/search')
def search_products():
    section = request.args.get('section')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    product_name = request.args.get('product_name')

    # Filter products based on search criteria
    products_query = Product.query

    if section:
        products_query = products_query.filter_by(section=section)

    if min_price:
        products_query = products_query.filter(Product.price >= min_price)

    if max_price:
        products_query = products_query.filter(Product.price <= max_price)

    if product_name:
        products_query = products_query.filter(Product.name.ilike(f'%{product_name}%'))

    products = products_query.all()

    return render_template('search_products.html', products=products)
