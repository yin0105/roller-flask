import math
from math import radians, sin, cos, asin, sqrt
from datetime import datetime

from app import db


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    cart_items = db.relationship('CartItem', 
        foreign_keys='CartItem.order_id', backref='order', lazy='dynamic')
    incoming_orders = db.relationship('IncomingOrder', 
        foreign_keys='IncomingOrder.order_id', backref='order', lazy='dynamic', cascade='all, delete-orphan')
    created_on = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # 'buyer' property defined in User.orders via backref.
    # 'suppliers' property defined in Company.orders via backref.

    def __repr__(self):
        return '<Order {}>'.format(self.buyer_id)

    def get_currency(self):
        for cart_item in self.cart_items:
            if any(cart_item.currency for cart_item in self.cart_items):
                currency = cart_item.currency
                return currency

    def count_total_items(self):
        total_items = 0
        for cart_item in self.cart_items:
            total_items = sum(cart_item.quantity for cart_item in self.cart_items)
        return total_items

    def count_total_amount(self):
        total_amount = 0
        for cart_item in self.cart_items:
            total_amount = sum(cart_item.ttl_amount for cart_item in self.cart_items)
            return total_amount


class IncomingOrder(db.Model):
    __tablename__ = 'incoming_order'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    cart_items = db.relationship('CartItem', 
        foreign_keys='CartItem.incoming_order_id', backref='incoming_order', lazy='dynamic')
    deliveries = db.relationship('Delivery', 
        foreign_keys='Delivery.incoming_order_id', backref='incoming_order', lazy='dynamic', cascade='all, delete')
    created_on = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # 'supplier' property defined in Company.incoming_orders via backref.
    # 'order' property defined in Order.incoming_orders via backref

    def __repr__(self):
        return '<IncomingOrder {}>'.format(self.company_id)

    def get_currency(self):
        for cart_item in self.cart_items:
            if any(cart_item.currency for cart_item in self.cart_items):
                currency = cart_item.currency
                return currency

    def count_supplier_total_items(self):
        total_items = 0
        for cart_item in self.cart_items:
            total_items = sum(cart_item.quantity for cart_item in self.cart_items)
        return total_items

    def count_supplier_total_amount(self):
        total_amount = 0
        for cart_item in self.cart_items:
            total_amount = sum(cart_item.ttl_amount for cart_item in self.cart_items)
            return total_amount

    # Get distance between collect and dropoff for delivery request
    def get_distance(self):
        lat1 = self.supplier.lat
        lon1 = self.supplier.lon
        lat2 = self.order.buyer.lat
        lon2 = self.order.buyer.lon
        radius = 6371 # approximate value for spherical Earth formula in km
        dlat = math.radians(lat2-lat1)
        dlon = math.radians(lon2-lon1)
        a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1))\
             * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        d = radius * c
        return round(d, 2)
