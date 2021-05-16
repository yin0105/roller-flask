from flask import flash, render_template, redirect, url_for
from flask_login import current_user, login_required
from datetime import datetime

from app import db
from app.clinical_note import clinical_note_blueprint
from app.clinical_note.forms import CreateClinicalNoteForm
from app.clinical_note.models import ClinicalNote
from app.booking.models import Booking
from app.consultation.models import Consultation
from app.health_record.models import HealthRecord
from app.user.models import User


@clinical_note_blueprint.route('/consultation_id/<int:consultation_id>', methods=['GET', 'POST'])
@login_required
def create(consultation_id):
	consultation = Consultation.query.get_or_404(consultation_id)
	booking = Booking.query.get_or_404(consultation.booking_id)
	customer = consultation.customer
	health_record = HealthRecord.query.get_or_404(customer.id)
	provider = current_user
	time_now = datetime.now()

	form=CreateClinicalNoteForm()
	if form.validate_on_submit():
		clinical_note=ClinicalNote(customer_id=customer.id,
									provider_id=provider.id,
									consultation_id=consultation.id,
									body=form.body.data,
									last_edited=time_now)
		db.session.add(clinical_note)

		booking.consulted = True
		booking.has_ended = False
		
		db.session.commit()
		flash('Clinical note created')
		return redirect(url_for('medical_cert.create', consultation_id=consultation.id))
	return render_template('clinical_note/telemed_create.html', title='Consulting', 
																	booking=booking, 
																	customer=customer,
																	consultation=consultation,
																	form=form)
