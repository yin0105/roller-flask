from app import db
from datetime import datetime


class Booking(db.Model):
	__tablename__ = 'booking'
	id = db.Column(db.Integer, primary_key=True)
	customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
	provider_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	note = db.Column(db.String(128))
	booking_type = db.Column(db.String(128))
	consulted = db.Column(db.Boolean(), default=False)
	cancelled = db.Column(db.Boolean(), default=False)
	has_ended = db.Column(db.Boolean(), default=False)
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	# 'customer' property defined in User.bookings_sent via backref.
	# 'clinic' property defined in Company.bookings_received via backref.
	# 'provider' property defined in User.bookings_accepted via backref.
	

	def __repr__(self):
		return '<Booking {}>'.format(self.customer_id)
