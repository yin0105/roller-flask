from flask import flash, render_template, redirect, url_for, request
from flask_login import current_user, login_required
from datetime import datetime

from app import db
from app.prescription import prescription_blueprint
from app.prescription.forms import PrescriptionForm
from app.prescription.models import Prescription
from app.booking.models import Booking
from app.consultation.models import Consultation
from app.currency.models import Currency
from app.health_record.models import HealthRecord
from app.product.models import Product
from app.receipt.models import Receipt
from app.user.models import User


@prescription_blueprint.route('/consultation_id/<int:consultation_id>/prescription', methods=['GET', 'POST'])
@login_required
def create(consultation_id):
	consultation = Consultation.query.get_or_404(consultation_id)
	booking = Booking.query.get_or_404(consultation.booking_id)
	customer = consultation.customer
	health_record = HealthRecord.query.get_or_404(customer.id)
	provider = current_user
	time_now = datetime.now()

	form=PrescriptionForm()
	if request.method == 'POST':
		if form.validate_on_submit():
			provider=current_user
			prescription=Prescription(
				customer_id=customer.id, 
				provider_id=provider.id, 
				consultation_id=consultation.id,
				body=form.body.data)
			db.session.add(prescription)
			db.session.flush()
			product=form.product.data
			prescription.products.append(product)
			consultation.prescriptions.append(prescription)

		receipt = Receipt(provider_id=current_user.id,
							description='Tele-Consultation',
							price_amount='2000',
							discount_amount='200',
							service_amount='400',
							customer_paid_amount='1800',
							provider_received_amount='2000')
		db.session.add(receipt)
		current_user.provider_receipts.append(receipt)

		booking.consulted = True
		booking.has_ended = True

		db.session.commit()
		#flash('Medical certificate created')
		return redirect(url_for('health_record.show', user_id=customer.id, 
														health_record_id=health_record.id))
	return render_template('prescription/create.html', title='Consulting', 
														customer=customer, 
														booking=booking,  
														form=form)
