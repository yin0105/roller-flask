from app import db
from datetime import datetime


class MedicalCert(db.Model):
	__tablename__ = 'medical_cert'
	id = db.Column(db.Integer, primary_key=True)
	customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	provider_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	consultation_id = db.Column(db.Integer, db.ForeignKey('consultation.id'))
	num_of_unfit_days = db.Column(db.Integer)
	start_time = db.Column(db.Time())
	end_time = db.Column(db.Time())
	created_on = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	# 'customer' property defined in User.medical_cert_received via backref.
	# 'provider' property defined in User.medical_cert_provided via backref.
	# 'consultation' property defined in Consultation.medical_cert via backref.

	def __repr__(self):
		return '<MedicalCert {}>'.format(self.id)