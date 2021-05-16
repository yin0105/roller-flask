from datetime import datetime

from app import db


orders_subs = db.Table('orders_subs',
    db.Column('company_id', db.Integer, db.ForeignKey('company.id')),
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'))) 

class Company(db.Model):
	__tablename__ = 'company'
	id = db.Column(db.Integer, primary_key=True) 
	name = db.Column (db.String(64)) 
	about_us = db.Column(db.String(1280))
	logo_file = db.Column(db.String(128), nullable=False, default='default.jpg')
	building = db.Column (db.String(64))
	address = db.Column(db.String(128))
	unit_num = db.Column(db.String(32))
	country = db.Column (db.String(64))
	zip_code = db.Column(db.String(32))
	lat = db.Column(db.Float(precision=10, asdecimal=False, decimal_return_scale=None), nullable=True)
	lon = db.Column(db.Float(precision=10, asdecimal=False, decimal_return_scale=None), nullable=True)
	products = db.relationship('Product', 
		foreign_keys='Product.company_id', backref='supplier', lazy='dynamic', cascade='all, delete-orphan')
	cart_items = db.relationship('CartItem', 
		foreign_keys='CartItem.supplier_id', backref='supplier', lazy='dynamic', cascade='all, delete-orphan')
	orders = db.relationship('Order',
		secondary=orders_subs, backref=db.backref('suppliers', lazy='dynamic'))
	bookings_received = db.relationship('Booking', 
		foreign_keys='Booking.company_id', backref='clinic', lazy='dynamic', cascade='all, delete-orphan')
	incoming_orders = db.relationship('IncomingOrder',
		foreign_keys='IncomingOrder.company_id', backref='supplier', lazy='dynamic')
	created_on = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	# 'employees' property defined in User.workplaces via backref.
	# 'administrators' property defined in User.companies via backref.

	def __repr__(self):
		return '<Company {}>'.format(self.name, self.created_at)

	def count_orders_received(self):
		return self.incoming_orders.count()

	def count_bookings_received(self):
		from app.booking.models import Booking
		return self.bookings_received.filter(Booking.consulted==False).count()

