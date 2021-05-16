from datetime import datetime

from app import db


class Delivery(db.Model):
	__tablename__ = 'delivery'
	id = db.Column(db.Integer, primary_key=True)
	incoming_order_id = db.Column(db.Integer, db.ForeignKey('incoming_order.id'))
	collect_dist = db.Column(db.Float(precision=10, asdecimal=False, decimal_return_scale=None), nullable=True)
	dropoff_dist = db.Column(db.Float(precision=10, asdecimal=False, decimal_return_scale=None), nullable=True)
	unit = db.Column(db.String(128))
	accepted = db.Column(db.Boolean(), default=False)
	completed = db.Column(db.Boolean(), default=False)
	cancelled = db.Column(db.Boolean(), default=False)
	created_on = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	# 'incoming_order' property defined in IncomingOrder.deliveries via backref
	# 'couriers' property defined in User.deliveries via backref

	def __repr__(self):
		return '<Delivery {}>'.format(self.incoming_order_id)
