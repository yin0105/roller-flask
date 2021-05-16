from datetime import datetime

from app import db


class Receipt(db.Model):
    __tablename__ = 'receipt'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    provider_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    description = db.Column(db.String(960))
    currency = db.Column(db.String(128))
    price_amount = db.Column(db.Integer())
    discount_amount = db.Column(db.Integer())
    service_amount = db.Column(db.Integer())
    customer_paid_amount = db.Column(db.Integer())
    provider_received_amount = db.Column(db.Integer())
    created_on = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # 'customer' property defined in User.customer_receipts via backref.
    # 'provider' property defined in User.provider_receipts via backref.

    def __repr__(self):
        return '<Receipt {}>'.format(self.brand, self.model)
