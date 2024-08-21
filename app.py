
######################
from flask import Flask, render_template, redirect, url_for, flash, Blueprint
#from views import auth  # Import your auth blueprint here

from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin
from flask_caching import Cache
from redis import Redis
from celery_tasks import celery


from flask_login import LoginManager, login_required
#from flask_user import roles_required

from views.store_manager import store_manager_bp

from views.user import user_bp
from views.admin import admin_bp
from views.auth import auth_bp

from extensions import db

app = Flask(__name__)

app.config['EXPORT_PATH'] =  'D:\\Sanchay\\Desktop\\iit madras\\appdev2\\GS\\'


# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:/Sanchay/Desktop/iit madras/appdev2/GS/instance/database.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# Initialize the database
db.init_app(app)
from models.user import User, Role
from models.category import Category

app.register_blueprint(user_bp)
app.register_blueprint(store_manager_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(auth_bp)

# # Initialize admin credentials
from models.user import User, Role
with app.app_context():
    db.create_all()
    
# Create Flask-Security user data store
user_datastore = SQLAlchemyUserDatastore(db, User, Role)

#security = Security(app, user_datastore)

#

app.config.from_pyfile('config/config.py')
app.config['CACHE_TYPE'] = 'simple'  # You can choose other caching mechanisms
cache = Cache(app)

# Use cache with specific routes or views to improve performance
#redis_client = Redis(host='localhost', port=6379, db=0)

#app.config.from_object('config.Config') #as already done above in the code by app.config
#


# Define routes for different dashboards
@app.route('/')
def base():
    return render_template('index.html')

# @app.route('/user_dashboard')
# def user_dashboard():
#     return render_template('user_dashboard.html')

# @app.route('/store_manager_dashboard')
# def store_manager_dashboard():
#     return render_template('store_manager_dashboard.html')

# @app.route('/admin_dashboard')
# def admin_dashboard():
#     return render_template('admin_dashboard.html')



if __name__ == '__main__':

    app.run(debug=True)

