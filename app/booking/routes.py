import os
import stripe

from flask import flash, render_template, redirect, url_for, session
from flask_login import current_user, login_required

from app import db
from app.booking import booking_blueprint
from app.booking.models import Booking
from app.company.models import Company
from app.booking.forms import TelemedBookingForm
from app.user.models import User


stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
checkout_public_key = os.environ.get('STRIPE_PUBLIC_KEY')
endpoint_secret = os.environ.get('STRIPE_END_POINT_SECRET')


@booking_blueprint.route('/user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def dashboard(user_id):
	user = User.query.get_or_404(user_id)
	bookings_sent = user.bookings_sent.filter(Booking.consulted==False).order_by(Booking.timestamp.desc())
	for company in user.workplaces:
		bookings_received = company.bookings_received.order_by(Booking.timestamp.desc())
		bookings_accepted = user.bookings_accepted.filter(Booking.company_id==company.id).order_by(Booking.timestamp.desc())
	if current_user.phone != None:
		return render_template('booking/dashboard.html', title='Booking',
															user=user, 
															bookings_sent=bookings_sent)
	elif current_user.phone == None:
		return redirect(url_for('user.update', user_id=current_user.id, 
												username=current_user.username))


@booking_blueprint.route('/create_booking/company_id/<int:company_id>', methods=['GET', 'POST'])
@login_required
def create(company_id):
	company = Company.query.get_or_404(company_id)
	form=TelemedBookingForm()
	if form.validate_on_submit():
		booking=Booking(
			customer_id=current_user.id, 
			company_id=company.id, 
			booking_type=form.booking_type.data,
			note=form.note.data)
		db.session.add(booking)
		db.session.commit()
		#flash('Booking created')
		return redirect(url_for('booking.dashboard', user_id=current_user.id))
	return render_template('booking/create.html', title='Booking Teleconsult', form=form)


@booking_blueprint.route('/delete_booking/<int:booking_id>/user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def delete(booking_id, user_id):
	user = User.query.filter(User.id == int(user_id)).first_or_404()
	booking = Booking.query.get_or_404(booking_id)
	booking.cancelled = True
	db.session.delete(booking)
	db.session.commit()
	flash('Booking cancelled')
	return redirect(url_for('booking.dashboard', user_id=user.id))
