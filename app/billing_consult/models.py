from datetime import datetime

from app import db


class ConsultBill(db.Model):
    __tablename__ = 'consult_bill'
    id = db.Column(db.Integer, primary_key=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    currency = db.Column(db.String(128))
    amount = db.Column(db.Integer())
    feature_picture = db.Column(db.String(64), nullable=True, default='default.jpeg') 
    pictures = db.relationship('Picture', 
        foreign_keys='Picture.product_id', backref='product', lazy='dynamic', cascade='all, delete-orphan')
    created_on = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # 'provider' property defined in User.issued_consult_bill via backref.
    # 'company' property defined in Company.consult_bill via backref.
    # 'customer' property defined in User.paid_consult_bill via backref.
    