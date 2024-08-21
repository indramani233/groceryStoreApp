from extensions import db
#import app
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin

user_roles = db.Table(
    'user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    roles = db.relationship('Role', secondary=user_roles, backref=db.backref('users', lazy='dynamic'))
    is_approved = db.Column(db.Boolean, default=False)  # Example boolean field for approval status
    active = db.Column(db.Boolean(), default=True)
    is_admin = db.Column(db.Boolean(), default=False)
    is_store_manager = db.Column(db.Boolean(), default=False)

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)


# Create an admin user within the application context
    # with app.app_context():
    #     db.create_all()
        
    #     admin = User(username='admin', password='admin_password', is_admin=True, is_store_manager=False)
    #     db.session.add(admin)
    #     db.session.commit()
# # Initialize admin credentials (Ensure this block is executed after the models are created)
#admin = User(username='admin', password='admin_password', is_admin=True, is_store_manager=False)
#db.session.add(admin)
# db.session.commit()

# # Create Flask-Security user data store
# user_datastore = SQLAlchemyUserDatastore(db, User, Role)
# security = Security(app, user_datastore)