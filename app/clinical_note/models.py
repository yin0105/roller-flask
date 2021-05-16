from app import db
from datetime import datetime


class ClinicalNote(db.Model):
	__tablename__ = 'clinical_note'
	id = db.Column(db.Integer, primary_key=True)
	customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	provider_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	consultation_id = db.Column(db.Integer, db.ForeignKey('consultation.id'))
	body = db.Column(db.String(128))
	created_on = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	last_edited = db.Column(db.DateTime, default=datetime.utcnow)
	# 'customer' property defined in User.clinical_note_received via backref.
	# 'provider' property defined in User.clinical_note_provided via backref.
	# 'consultation' property defined in Consultation.clinical_note via backref.

	def __repr__(self):
		return '<ClinicalNote {}>'.format(self.id)
