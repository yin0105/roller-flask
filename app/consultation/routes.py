from flask import flash, render_template, redirect, url_for
from flask_login import current_user, login_required
from datetime import datetime

from app import db
from app.consultation import consultation_blueprint
from app.consultation.models import Consultation
from app.consultation.forms import AddProviderForm
from app.booking.models import Booking
from app.health_record.models import HealthRecord
from app.user.models import User


@consultation_blueprint.route('/create/booking_id/<int:booking_id>', methods=['GET', 'POST'])
@login_required
def dashboard(booking_id):
	booking = Booking.query.get_or_404(booking_id)
	customer = booking.customer
	health_record = HealthRecord.query.get_or_404(customer.id)
	provider = current_user

	consultation=Consultation(booking_id=booking.id, 
								customer_id=customer.id, 
								primary_provider_id=provider.id,  
								health_record_id=health_record.id)
	db.session.add(consultation)
	consultation.providers.append(provider)
	db.session.flush()

	booking.provider = provider
	booking.consulted = True
	booking.has_ended = False

	health_record.consultations.append(consultation)
	db.session.commit()
	if provider.phone != None:
		return render_template('consultation/dashboard.html', title='Consulting', 
																booking_id=booking.id, 
																consultation=consultation)
	elif provider.phone == None:
		flash('Please provide your NRIC, adddress and mobile phone.')
		return redirect(url_for('user.update', user_id=provider.id, 
												username=provider.username))


@consultation_blueprint.route('/add_provider/consultation_id/<int:consultation_id>/customer/<customer>', methods=['GET', 'POST'])
@login_required
def add_provider(consultation_id, customer):
	customer = User.query.filter_by(username=customer).first_or_404()
	print(f'Customer: {customer.username}')
	consultation = Consultation.query.get_or_404(consultation_id)
	form = AddProviderForm()
	if form.validate_on_submit():
		provider = User.query.filter_by(email=form.email.data).first()
		consultation.providers.append(provider)
		db.session.commit()
		flash('Provider added to consultation')
		return redirect(url_for('health_record.show',
								health_record_id=consultation.health_record_id,
								user_id=customer.id))
	return render_template('consultation/add_provider.html',
							title='Add Provider',
							consultation=consultation,
							form=form)


@consultation_blueprint.route('/delete/<int:consultation_id>/user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def delete(consultation_id, user_id):
	user = User.query.filter(User.id == int(user_id)).first_or_404()
	consultation = Consultation.query.get_or_404(consultation_id)
	health_record_id = consultation.health_record_id
	health_record = HealthRecord.query.get(int(health_record_id))
	health_record.consultations.remove(consultation)
	db.session.commit()
	flash('Consultation record removed')
	return redirect(url_for('health_record.show', user_id=user.id, health_record_id=health_record.id))

