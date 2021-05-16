from datetime import datetime

from app import db


class Currency(db.Model):
	__tablename__ = 'currency'
	id = db.Column(db.Integer, primary_key=True) 
	name = db.Column(db.String(64), index=True, unique=True) 
	code = db.Column(db.String(32), index=True, unique=True)
	sign = db.Column(db.String(32), index=True, unique=True)
	value = db.Column(db.String(32), index=True, unique=True)
	format_str = db.Column(db.String(32), index=True, unique=True)
	unicode_hex = db.Column(db.String(32), index=True, unique=True) 
	unicode_decimal = db.Column(db.String(32), index=True, unique=True)
	created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)

	def __repr__(self):
		return '<Currency {}>'.format(self.name)

	def currency_count():
		currencies = Currency.query.all()
		count = 0
		for currency in currencies:
			count += 1
		return count

		
