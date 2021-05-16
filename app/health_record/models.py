from app import db
from datetime import datetime


class HealthRecord(db.Model):
	__tablename__ = 'health_record'
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	consultations = db.relationship('Consultation', 
		foreign_keys='Consultation.health_record_id', backref='health_record', lazy='dynamic', cascade='all, delete-orphan')
	# 'owner' property defined in User.health_record via backref.

	def __repr__(self):
		return '<HealthRecord {}>'.format(self.user_id)