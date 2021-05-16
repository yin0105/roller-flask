from datetime import datetime

from app import db


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(64), index=True)
    model = db.Column(db.String(128), index=True)
    description = db.Column(db.String(960))
    currency = db.Column(db.String(128))
    amount = db.Column(db.Integer())
    discount = db.Column(db.Integer())
    quantity = db.Column(db.String(128))
    feature_picture = db.Column(db.String(64), nullable=True, default='default.jpeg') 
    pictures = db.relationship('Picture', 
        foreign_keys='Picture.product_id', backref='product', lazy='dynamic', cascade='all, delete-orphan')
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    created_on = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # 'cart_item' property defined in CartItem.product via backref.
    # 'supplier' property defined in Company.products via backref.

    def __repr__(self):
        return '<Product {}>'.format(self.brand, self.model)

def get_product():
    return Product.query.all()


class Picture(db.Model):
    __tablename__ = 'picture'
    id = db.Column(db.Integer, primary_key=True)
    picture_file = db.Column(db.String(64), nullable=False, default='default.jpeg')
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    # 'product' property defined in Product.pictures via backref.

    def __repr__(self):
        return '<Picture {}>'.format(self.picture_file, self.product_id)
