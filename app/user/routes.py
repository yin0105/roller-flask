from flask import flash, render_template, request, redirect, url_for, \
    current_app, send_from_directory, abort, session
from werkzeug.utils import secure_filename
from flask_login import current_user, login_required

import os
import secrets
from PIL import Image
from geopy.geocoders import Nominatim

from app import db
from app.user import user_blueprint
from app.user.forms import UpdateProfileForm, UpdateDoctorProfileForm, UploadSelfieForm
from app.user.models import User
from app.booking.models import Booking
from app.cart.models import Cart
from app.company.models import Company
from app.currency.models import Currency
from app.delivery.models import Delivery
from app.feedback.models import Feedback
from app.health_record.models import HealthRecord
from app.medical_cert.models import MedicalCert
from app.order.models import Order
from app.product.models import Product


def check_superadmin():
    if not current_user.is_superadmin:
        abort(403)


@user_blueprint.route('/dashboard/user_id/<int:user_id>')
@login_required
def dashboard(user_id):
    if current_user.profession == 'Doctor' and current_user.mreg == None:
        return redirect(url_for('user.update', user_id=current_user.id))

    user = User.query.filter(User.id==int(user_id)).first_or_404()
    users = User.query.filter(User.profession=='Others').all()

    companies = Company.query.all()
    currencies = Currency.query.all()

    # Bookings for teleconsult
    bookings_sent_all = Booking.query.filter(Booking.consulted==False).order_by(Booking.timestamp.desc())
    bookings_sent = user.bookings_sent.filter(Booking.consulted==False).order_by(Booking.timestamp.desc())

    cart_id = current_user.id
    cart = Cart.query.get_or_404(cart_id)
    carts = Cart.query.all()

    deliveries = Delivery.query.all()
    new_deliveries = Delivery.query.filter(Delivery.accepted==False).all()

    doctors = User.query.filter(User.profession=='Doctor').all()
    feedbacks = Feedback.query.all()

    medical_certs = MedicalCert.query.all()

    orders = Order.query.join(Order.buyer).filter(User.id==user_id)
    total_orders = Order.query.all()

    products = Product.query.all()

    session['CART'] = cart.count_total_items()
    print('Session Cart Items: ' + str(session['CART']))

    session['CHAT'] = current_user.unread_chats()
    print('Session Unread Messages: ' + str(session['CHAT']))

    session['ORDERS'] = orders.count()
    print('Session Orders: ' + str(session['ORDERS']))

    if current_user.is_superadmin:
        return render_template('admin/dashboard.html',
                                title='Admin Dashboard', 
                                bookings_sent=bookings_sent, 
                                bookings_sent_all=bookings_sent_all,
                                cart=cart,
                                carts=carts,
                                companies=companies, 
                                currencies=currencies,
                                deliveries=deliveries,
                                new_deliveries=new_deliveries,
                                doctors=doctors,
                                feedbacks=feedbacks,
                                medical_certs=medical_certs,
                                orders=orders,
                                total_orders=total_orders,
                                products=products,
                                user=user,
                                users=users)
    else:
        return render_template('user/dashboard.html',
                                title='User Dashboard', 
                                bookings_sent=bookings_sent, 
                                bookings_sent_all=bookings_sent_all,
                                cart=cart, 
                                carts=carts,
                                companies=companies,
                                currencies=currencies,
                                deliveries=deliveries,
                                new_deliveries=new_deliveries,
                                feedbacks=feedbacks,
                                products=products,
                                user=user,
                                users=users)


@user_blueprint.route('/profile/user_id/<int:user_id>')
@login_required
def profile(user_id):
    user = User.query.filter(User.id == int(user_id)).first_or_404()
    selfie_file = url_for('static', filename='uploads/selfie_img/' + current_user.selfie_file)
    cart_id = current_user.id
    cart = Cart.query.get_or_404(cart_id)

    session['CART'] = cart.count_total_items()
    print('Session Cart Items: ' + str(session['CART']))
    session['CHAT'] = current_user.unread_chats()
    print('Session Unread Messages: ' + str(session['CHAT']))
    return render_template('user/profile.html',
        title='User Profile',
        user=user,
        selfie_file=selfie_file)


@user_blueprint.route('/update/user_id/<user_id>', methods=['GET', 'POST'])
@login_required
def update(user_id):
    user = User.query.filter(User.id == int(user_id)).first_or_404()
    selfie_file = url_for('static', filename='uploads/selfie_img/' + current_user.selfie_file)

    if current_user.is_doctor:
        form = UpdateDoctorProfileForm(current_user.username, current_user.email)
        if form.validate_on_submit():
            current_user.username = form.username.data
            current_user.designation = form.designation.data
            current_user.given_name = form.given_name.data
            current_user.last_name = form.last_name.data
            current_user.email = form.email.data
            current_user.nric = form.nric.data
            current_user.phone = form.phone.data
            current_user.practice = form.practice.data
            current_user.mreg_type = form.mreg_type.data
            current_user.mreg = form.mreg.data
            current_user.about_me = form.about_me.data
            # User address
            current_user.building = form.building.data
            current_user.address = form.address.data
            current_user.unit_num = form.unit_num.data
            current_user.country = form.country.data
            current_user.zip_code = form.zip_code.data
            # Geocoder
            geo_address = request.form['address'] + ', ' + form.country.data + ' ' + str(form.zip_code.data)
            print(f'{geo_address}')
            geolocator = Nominatim(user_agent='zoz')
            location = geolocator.geocode(geo_address)
            lat = location.latitude
            lon = location.longitude
            # User lat lon
            current_user.lat = lat
            current_user.lon = lon
            
            db.session.commit()
            flash('Your profile is updated.')
            return redirect(url_for('user.profile',
                user_id=current_user.id,
                username=current_user.username))
        elif request.method == 'GET':
            form.username.data = current_user.username
            form.designation.data = current_user.designation
            form.given_name.data = current_user.given_name
            form.last_name.data = current_user.last_name
            form.email.data = current_user.email
            form.nric.data = current_user.nric
            form.phone.data = current_user.phone
            form.practice.data = current_user.practice
            form.mreg_type.data = current_user.mreg_type
            form.mreg.data = current_user.mreg
            form.about_me.data = current_user.about_me
            # User address
            form.building.data = current_user.building
            form.address.data = current_user.address
            form.unit_num.data = current_user.unit_num
            form.country.data = current_user.country
            form.zip_code.data = current_user.zip_code
            form.lat.data = current_user.lat
            form.lon.data = current_user.lon
        return render_template('user/update.html',
                                title='Edit Profile',
                                form=form,
                                user=user,
                                selfie_file=selfie_file)
    else:
        form = UpdateProfileForm(current_user.username, current_user.email)
        if form.validate_on_submit():
            current_user.username = form.username.data
            current_user.designation = form.designation.data
            current_user.given_name = form.given_name.data
            current_user.last_name = form.last_name.data
            current_user.email = form.email.data
            current_user.nric = form.nric.data
            current_user.phone = form.phone.data
            current_user.about_me = form.about_me.data
            # User address
            current_user.building = form.building.data
            current_user.address = form.address.data
            current_user.unit_num = form.unit_num.data
            current_user.country = form.country.data
            current_user.zip_code = form.zip_code.data
            # Geocoder
            geo_address = request.form['address'] + ', ' + form.country.data + ' ' + str(form.zip_code.data)
            print(f'{geo_address}')
            geolocator = Nominatim(user_agent='zoz')
            location = geolocator.geocode(geo_address)
            lat = location.latitude
            lon = location.longitude
            # User lat lon
            current_user.lat = lat
            current_user.lon = lon

            db.session.commit()
            flash('Your profile is updated.')
            return redirect(url_for('user.profile', user_id=current_user.id))
        elif request.method == 'GET':
            form.username.data = current_user.username
            form.designation.data = current_user.designation
            form.given_name.data = current_user.given_name
            form.last_name.data = current_user.last_name
            form.email.data = current_user.email
            form.nric.data = current_user.nric
            form.phone.data = current_user.phone
            form.about_me.data = current_user.about_me
             # User address
            form.building.data = current_user.building
            form.address.data = current_user.address
            form.unit_num.data = current_user.unit_num
            form.country.data = current_user.country
            form.zip_code.data = current_user.zip_code
            form.lat.data = current_user.lat
            form.lon.data = current_user.lon
        return render_template('user/update.html',title='Edit Profile',
                                                    form=form,
                                                    user=user,
                                                    selfie_file=selfie_file)


@user_blueprint.route('/delete/user_id/<user_id>', methods=['GET', 'POST'])
@login_required
def delete(user_id):
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


def save_photo(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.config['SELFIE_IMG'], picture_fn)
    #picture_path = os.path.join(current_app.root_path, 'static/uploads/selfie_img', picture_fn)
    output_size = (250, 250)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


@user_blueprint.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadSelfieForm()
    if form.validate_on_submit():
        if form.photo.data:
            photo_file = secure_filename(save_photo(form.photo.data))
            current_user.selfie_file = photo_file
        db.session.commit()
        flash('Selfie has been saved.')
        return redirect(url_for('user.update', user_id=current_user.id))
    elif request.method == 'GET':
        selfie_file = url_for('user.get_selfie', filename=current_user.selfie_file)
    return render_template('user/upload_selfie.html', title='Upload Selfie',
                                                        selfie_file=selfie_file,
                                                        form=form)


@user_blueprint.route('/get_selfie/<filename>')
@login_required
def get_selfie(filename):
    try:
        print(filename)
        return send_from_directory(os.path.join(current_app.config['SELFIE_IMG']), filename)
    except FileNotFoundError:
        abort(404)

