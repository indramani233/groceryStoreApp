# models/category.py

from extensions import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    approval_required = db.Column(db.Boolean, default=False)  # New field for approval requirement

    def __repr__(self):
        return f"Category('{self.name}')"
