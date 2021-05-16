from app import db
from datetime import datetime


class Consultation(db.Model):
	__tablename__ = 'consultation'
	id = db.Column(db.Integer, primary_key=True)
	booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'))
	customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	primary_provider_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	health_record_id = db.Column(db.Integer, db.ForeignKey('health_record.id'))
	clinical_note = db.relationship('ClinicalNote', backref=db.backref('consultation', 
		lazy='joined', uselist=False, single_parent=True, cascade='all, delete-orphan'))
	prescriptions = db.relationship('Prescription',
		foreign_keys='Prescription.consultation_id', backref='consultation', lazy='dynamic')
	medical_cert = db.relationship('MedicalCert', backref=db.backref('consultation', 
		lazy='joined', uselist=False, single_parent=True, cascade='all, delete-orphan'))
	created_on = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	# 'customer' property defined in User.consultations_received via backref.
	# 'primary_provider' property defined in User.consultations_provided via backref.
	# 'providers' property defined in User.consultations via backref.

	def __repr__(self):
		return '<Consultation {}>'.format(self.booking_id)
