from flask import flash, render_template, redirect, url_for, request
from flask_login import current_user, login_required
from datetime import datetime

from app import db
from app.medical_cert import medical_cert_blueprint
from app.medical_cert.forms import CreateUnfitMedicalCertForm
from app.medical_cert.models import MedicalCert
from app.booking.models import Booking
from app.consultation.models import Consultation
from app.health_record.models import HealthRecord
from app.prescription.models import Prescription
from app.user.models import User


@medical_cert_blueprint.route('/create_medical_cert/consultation_id/<int:consultation_id>', methods=['GET', 'POST'])
@login_required
def create(consultation_id):
	consultation = Consultation.query.get_or_404(consultation_id)
	booking = Booking.query.get_or_404(consultation.booking_id)
	customer = consultation.customer
	health_record = HealthRecord.query.get_or_404(customer.id)
	provider = current_user
	time_now = datetime.now()
	
	form=CreateUnfitMedicalCertForm()
	if form.validate_on_submit():
		provider = current_user
		medical_cert=MedicalCert(  
			customer_id=customer.id, 
			provider_id=provider.id, 
			consultation_id=consultation.id, 
			num_of_unfit_days=form.num_of_unfit_days.data)
		db.session.add(medical_cert)

		booking.consulted = True
		booking.has_ended = False

		db.session.commit()
		#flash('Medical certificate created')
		return redirect(url_for('prescription.create', consultation_id=consultation.id))
	return render_template('medical_cert/create.html', title='Consulting', 
																	customer=customer, 
																	booking=booking, 
																	form=form)

