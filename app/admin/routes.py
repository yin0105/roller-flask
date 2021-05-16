from flask import flash, render_template, request, redirect, url_for, \
	abort, current_app, session
from flask_login import current_user, login_required

from app import db
from app.admin import admin_blueprint

from app.booking.models import Booking
from app.cart.models import Cart
from app.chat.models import Chats
from app.company.models import Company
from app.consultation.models import Consultation
from app.currency.models import Currency
from app.delivery.models import Delivery
from app.feedback.models import Feedback
from app.health_record.models import HealthRecord
from app.medical_cert.models import MedicalCert
from app.order.models import Order, IncomingOrder
from app.product.models import Product
from app.receipt.models import Receipt
from app.receipt.forms import CreateReceiptForm, UpdateReceiptForm
from app.user.models import User


def check_superadmin():
	if not current_user.is_superadmin:
		abort(403)


ROWS_PER_PAGE = 10


@admin_blueprint.route('/bookings/show_all')
@login_required
def booking():
	check_superadmin()
	bookings = Booking.query.filter(Booking.consulted==False).all()
	return render_template('admin/bookings.html', title='Bookings', bookings=bookings)


@admin_blueprint.route('/delete_bookings/<int:booking_id>', methods=['GET', 'POST'])
@login_required
def delete_booking(booking_id):
	check_superadmin()
	booking = Booking.query.get_or_404(booking_id)
	db.session.delete(booking)
	db.session.commit()
	flash('Delete booking')
	return redirect(url_for('admin.booking'))


@admin_blueprint.route('/carts/show_all')
@login_required
def cart():
	check_superadmin()
	carts = Cart.query.all()
	return render_template('admin/carts.html', title='Carts', carts=carts)


@admin_blueprint.route('/show/cart_id/<int:cart_id>')
@login_required
def show_cart(cart_id):
	check_superadmin()
	cart = Cart.query.get_or_404(cart_id)
	user = cart.owner
	currency = cart.get_currency()
	total_items = cart.count_total_items()
	total_amount = cart.count_total_amount()
	return render_template('cart/dashboard.html', title='Cart',
													cart=cart, user=user,
													currency=currency,
													total_items=total_items,
													total_amount=total_amount)


@admin_blueprint.route('/companies/show_all')
@login_required
def company():
	check_superadmin()
	companies = Company.query.all()
	return render_template('admin/companies.html', title='Companies', companies=companies)


@admin_blueprint.route('/delete_company/company_id/<int:company_id>', methods=['GET', 'POST'])
@login_required
def delete_company(company_id):
    company = Company.query.get_or_404(company_id)
    db.session.delete(company)
    db.session.commit()
    flash('Company removed.')
    return redirect(url_for('admin.company'))


@admin_blueprint.route('/consultations/show_all', methods=['GET', 'POST'])
@login_required
def consultation():
	check_superadmin()
	consultations = Consultation.query.order_by(Consultation.created_on.desc()).all()
	return render_template('admin/consultations.html', title='Consultations', consultations=consultations)


@admin_blueprint.route('/delete_consultation/<int:consultation_id>', methods=['GET', 'POST'])
@login_required
def delete_consultation(consultation_id):
	check_superadmin()
	consultation = Consultation.query.get_or_404(consultation_id)
	db.session.delete(consultation)
	db.session.commit()
	flash('Delete consultation')
	return redirect(url_for('admin.consultation'))


@admin_blueprint.route('/currencies/show_all')
@login_required
def currency():
	check_superadmin()
	currencies = Currency.query.order_by(Currency.created_at.desc()).all()
	print(f'Currencies: {Currency.currency_count()}')
	return render_template('admin/currencies.html', title='Currencies', currencies=currencies)


@admin_blueprint.route('/deliveries/show_all')
@login_required
def delivery():
	check_superadmin()
	deliveries = Delivery.query.order_by(Delivery.created_on.desc()).all()
	new_deliveries = Delivery.query.filter(Delivery.accepted==False).all()
	past_deliveries = Delivery.query.filter(Delivery.completed==True and Delivery.cancelled==True).all()
	return render_template('admin/deliveries.html', title='Delivery Jobs',
													deliveries=deliveries,
													new_deliveries=new_deliveries,
													past_deliveries=past_deliveries)


@admin_blueprint.route('/deliveries/show/job/<int:delivery_id>', methods=['GET', 'POST'])
@login_required
def show_delivery(delivery_id):
	check_superadmin()
	delivery = Delivery.query.get_or_404(delivery_id)
	return render_template('admin/show_delivery.html', title='Delivery Job', delivery=delivery)


@admin_blueprint.route('/deliveries/cancel/job/<int:delivery_id>', methods=['GET', 'POST'])
@login_required
def delete_delivery(delivery_id):
	check_superadmin()
	delivery = Delivery.query.get_or_404(delivery_id)
	delivery.couriers = []
	db.session.delete(delivery)
	db.session.commit()
	flash('Delivery job deleted.')
	return redirect(url_for('admin.delivery'))


@admin_blueprint.route('/doctors/show_all')
@login_required
def doctor():
	check_superadmin()
	# Set the pagination configuration
	page = request.args.get('page', 1, type=int)
	users = User.query.filter(User.profession=='Doctor').paginate(page=page, per_page=ROWS_PER_PAGE)
	next_url = url_for('admin.people', page=users.next_num) \
		if users.has_next else None
	prev_url = url_for('admin.people', page=users.prev_num) \
		if users.has_prev else None
	return render_template('admin/doctors.html', title='Doctors', users=users)


@admin_blueprint.route('/doctor_up/user_id/<int:user_id>', methods=['GET', 'POST'])
@login_required
def doctor_up(user_id):
	check_superadmin()
	user = User.query.get_or_404(user_id)
	user.is_physician = True
	db.session.commit()
	flash('User juiced up to Doctor.')
	return redirect(url_for('admin.doctor'))


@admin_blueprint.route('/remove_doctor/user_id/<int:user_id>', methods=['GET', 'POST'])
@login_required
def remove_doctor(user_id):
	check_superadmin()
	user = User.query.get_or_404(user_id)
	cart = Cart.query.get_or_404(user_id)
	db.session.delete(cart)
	health_record = HealthRecord.query.get_or_404(user_id)
	db.session.delete(health_record)
	db.session.flush()
	db.session.delete(user)
	db.session.commit()
	flash('User removed.')
	return redirect(url_for('admin.doctor'))


@admin_blueprint.route('/feedbacks/show_all')
@login_required
def feedback():
	check_superadmin()
	feedbacks = Feedback.query.order_by(Feedback.created_on.desc()).all()
	return render_template('admin/feedback.html', title='Feedbacks', feedbacks=feedbacks)


@admin_blueprint.route('/delete_feedback/<int:feedback_id>', methods=['GET', 'POST'])
@login_required
def delete_feedback(feedback_id):
	check_superadmin()
	feedback = Feedback.query.get_or_404(feedback_id)
	db.session.delete(feedback)
	db.session.commit()
	return redirect(url_for('admin.feedback'))


@admin_blueprint.route('/health_records/show_all')
@login_required
def health_record():
	check_superadmin()
	health_records = HealthRecord.query.all()
	return render_template('admin/health_records.html', title='Health Records', health_records=health_records)


@admin_blueprint.route('/delete_health_record/health_record_id/<int:health_record_id>', methods=['GET', 'POST'])
@login_required
def delete_health_record(health_record_id):
	check_superadmin()
	health_record = HealthRecord.query.get_or_404(health_record_id)
	db.session.delete(health_record)
	db.session.delete(health_record)
	db.session.commit()
	flash('Health Record removed.')
	return redirect(url_for('admin.health_record'))


@admin_blueprint.route('/medical_certificates/show_all', methods=['GET', 'POST'])
@login_required
def medical_cert():
	check_superadmin()
	medical_certs = MedicalCert.query.order_by(MedicalCert.created_on.desc()).all()
	return render_template('admin/medical_certs.html', title='Medical Certs', medical_certs=medical_certs)


@admin_blueprint.route('/delete_medical_certificate/delete/<int:medical_cert_id>', methods=['GET', 'POST'])
@login_required
def delete_medical_cert(medical_cert_id):
	check_superadmin()
	medical_cert = MedicalCert.query.get_or_404(medical_cert_id)
	db.session.delete(medical_cert)
	db.session.commit()
	flash('Medical certificate deleted.')
	return redirect(url_for('admin.medical_cert'))


@admin_blueprint.route('/orders/show_all')
@login_required
def order():
	check_superadmin()
	orders = Order.query.order_by(Order.created_on.desc()).all()
	return render_template('admin/orders.html', title='Orders', orders=orders)


@admin_blueprint.route('/show_order/order_id/<int:order_id>/user_id/<int:user_id>', methods=['GET', 'POST'])
@login_required
def show_order(order_id, user_id):
	check_superadmin()
	order = Order.query.get_or_404(order_id)
	cart = Cart.query.join(Order.buyer).filter(User.id==user_id)
	currency = order.get_currency()
	total_items = order.count_total_items()
	total_amount = order.count_total_amount()
	return render_template('order/show.html', title='Order',
												order=order,
												cart=cart,
												currency=currency,
												total_items=total_items,
												total_amount=total_amount)


@admin_blueprint.route('/delete_order/order_id/<int:order_id>/purchaser_id/<int:user_id>', methods=['GET', 'POST'])
@login_required
def delete_order(order_id, user_id):
	check_superadmin()
	order = Order.query.get_or_404(order_id)
	user_id = order.buyer_id
	db.session.delete(order)
	db.session.commit()
	orders = Order.query.join(Order.buyer).filter(User.id==user_id)
	session['ORDERS'] = orders.count()
	return redirect(url_for('admin.order'))


@admin_blueprint.route('/users/show_all')
@login_required
def people():
	check_superadmin()
	# Set the pagination configuration
	page = request.args.get('page', 1, type=int)
	users = User.query.paginate(page=page, per_page=ROWS_PER_PAGE)
	next_url = url_for('admin.people', page=users.next_num) \
		if users.has_next else None
	prev_url = url_for('admin.people', page=users.prev_num) \
		if users.has_prev else None
	return render_template('admin/people.html', title='People', users=users)
	# {% for user in users.items %} see Jinja template


@admin_blueprint.route('/superadmin_up/user_id/<int:user_id>', methods=['GET', 'POST'])
@login_required
def superadmin_up(user_id):
	check_superadmin()
	user = User.query.get_or_404(user_id)
	user.is_superadmin = True
	db.session.commit()
	flash('User juiced up to superadmin.')
	return redirect(url_for('admin.people'))


@admin_blueprint.route('/superadmin_down/user_id/<int:user_id>', methods=['GET', 'POST'])
@login_required
def superadmin_down(user_id):
	check_superadmin()
	user = User.query.get_or_404(user_id)
	user.is_superadmin = False
	db.session.commit()
	flash('User juiced down to superadmin.')
	return redirect(url_for('admin.people'))


@admin_blueprint.route('/remove_people/user_id/<int:user_id>', methods=['GET', 'POST'])
@login_required
def remove_people(user_id):
	check_superadmin()
	user = User.query.get_or_404(user_id)
	cart = Cart.query.get_or_404(user_id)
	db.session.delete(cart)
	health_record = HealthRecord.query.get_or_404(user_id)
	db.session.delete(health_record)
	db.session.flush()
	db.session.delete(user)
	db.session.commit()
	flash('User removed.')
	return redirect(url_for('admin.people'))


@admin_blueprint.route('/products/show_all')
@login_required
def product():
	check_superadmin()
	products = Product.query.all()
	return render_template('admin/products.html', title='Products', products=products)


@admin_blueprint.route('/receipts/show_all')
@login_required
def receipt():
	check_superadmin()
	receipts = Receipt.query.all()
	return render_template('admin/receipts.html', title='Receipts', receipts=receipts)


@admin_blueprint.route('/create_receipt', methods=['GET', 'POST'])
@login_required
def create_receipt():
	form=CreateReceiptForm()
	if form.validate_on_submit():
		dollar = form.price_amount.data
		price_amount = int(dollar)
		receipt=Receipt(
			description=form.description.data,
			currency=form.currency.data,
			price_amount=form.price_amount.data,
			discount_amount=form.discount_amount.data,
			service_amount=form.service_amount.data)
		db.session.add(receipt)
		receipt.customer_paid_amount = int(receipt.price_amount)-int(receipt.discount_amount)
		receipt.provider_received_amount = int(receipt.price_amount)
		db.session.commit()
		flash('Receipt created')
		return redirect(url_for('admin.receipt'))
	return render_template('receipt/create.html', title='Create Receipt', form=form)



@admin_blueprint.route('/update_receipt/<int:receipt_id>', methods=['GET', 'POST'])
@login_required
def update_receipt(receipt_id):
	receipt = Receipt.query.get_or_404(receipt_id)
	form = UpdateReceiptForm()
	if form.validate_on_submit():
		receipt.description = form.description.data
		receipt.currency = form.currency.data
		receipt.price_amount = form.price_amount.data
		receipt.discount_amount = form.discount_amount.data
		receipt.service_amount = form.service_amount.data
		receipt.customer_paid_amount = int(form.customer_paid_amount.data) - int(receipt.discount_amount)
		receipt.provider_received_amount = int(receipt.price_amount)
		db.session.commit()
		flash('Receipt information updated.')
		return redirect(url_for('admin.receipt'))
	elif request.method == 'GET':
		form.description.data = receipt.description
		form.currency.data = receipt.currency
		form.price_amount.data = receipt.price_amount
		form.discount_amount.data = receipt.discount_amount
		form.service_amount.data = receipt.service_amount
		form.customer_paid_amount.data = receipt.customer_paid_amount
		form.provider_received_amount.data = receipt.provider_received_amount
	return render_template('receipt/update.html', title='Edit Receipt', form=form)


@admin_blueprint.route('/delete_receipt/<int:receipt_id>', methods=['GET', 'POST'])
@login_required
def delete_receipt(receipt_id):
	check_superadmin()
	receipt = Receipt.query.get_or_404(receipt_id)
	db.session.delete(receipt)
	db.session.commit()
	flash('Receipt removed.')
	return redirect(url_for('admin.receipt'))
