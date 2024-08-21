# Example routes in home.py
from flask import Blueprint

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def index():
    return 'Welcome to the homepage'

# Add more routes as needed
