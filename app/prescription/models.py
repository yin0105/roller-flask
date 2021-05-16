from app import db
from datetime import datetime


products_prescriptions = db.Table('products_prescriptions',
    db.Column('product_id', db.Integer, db.ForeignKey('product.id')),
    db.Column('prescription_id', db.Integer, db.ForeignKey('prescription.id')))


class Prescription(db.Model):
	__tablename__ = 'prescription'
	id = db.Column(db.Integer, primary_key=True)
	customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	provider_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	consultation_id = db.Column(db.Integer, db.ForeignKey('consultation.id'))
	products = db.relationship('Product',
		secondary=products_prescriptions, backref=db.backref('prescriptions', lazy='dynamic'))
	body = db.Column(db.String(960))
	created_on = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	# 'customer' property defined in User.prescription_received via backref.
	# 'provider' property defined in User.prescription_provided via backref.
	# 'consultation' property defined in Consultation.prescriptions via backref.
	
	def __repr__(self):
		return '<Prescription {}>'.format(self.id)
