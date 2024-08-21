# models/product.py

from extensions import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('products', lazy=True))
    quantity_available = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return f"Product('{self.title}', '{self.description}', '{self.cost}')"
