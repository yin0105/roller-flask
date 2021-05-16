import csv
import pandas as pd
from flask import flash, render_template, request, redirect, url_for, \
    current_app, send_from_directory, abort, jsonify, session
from werkzeug.utils import secure_filename
from flask_login import current_user, login_required
from geopy.geocoders import Nominatim

import os
import secrets
from PIL import Image

from app import db
from app.company import company_blueprint
from app.company.forms import CreateCompanyForm, UpdateCompanyForm, AddUserForm, UploadLogoForm
from app.company.models import Company
from app.product.models import Product
from app.product.forms import CreateProductForm
from app.user.models import User
from app.order.models import Order, IncomingOrder
from app.cart.models import CartItem
from app.booking.models import Booking


@company_blueprint.route('/create_company', methods=['GET', 'POST'])
@login_required
def create():
    form = CreateCompanyForm()
    if form.validate_on_submit():
        name = form.name.data
        about_us = form.about_us.data
        building = form.building.data
        unit_num = form.unit_num.data
        address = form.address.data
        country = form.country.data
        zip_code = form.zip_code.data
        # Geocoder
        geo_address = request.form['address'] + ', ' + form.country.data + ' ' + str(form.zip_code.data)
        print(f'{geo_address}')
        geolocator = Nominatim(user_agent='connected')
        location = geolocator.geocode(geo_address)
        lat = location.latitude
        lon = location.longitude

        company = Company(
            name=name,
            building = building,
            address = address,
            unit_num = unit_num,
            zip_code = zip_code,
            country = country,
            lat=lat,
            lon=lon)
        db.session.add(company)
        db.session.flush()
        company.administrators.append(current_user)
        company.employees.append(current_user)
        db.session.commit()

        # create first dataframe with dictionary
        df1 = pd.read_csv('companies.csv', header=0)
        for index, row in df1.iterrows():
            print(row['ID'], row['NAME'], row['LAT'], row['LON'])
            if str(row['ID']) == str(company.id):
                row['NAME'] = name
                row['LAT'] = lat
                row['LON'] = lon
        # create second dataframe with dictionary
        df2 = pd.DataFrame({
            'ID': [company.id],
            'NAME': [name],
            'LAT': [lat],
            'LON': [lon]})
        dff = df1.append(df2, ignore_index=True)
        dff.to_csv(r'companies.csv', index=False)

        flash('Company created.')
        return redirect(url_for('company.workplace', user_id=current_user.id))
    return render_template(
        'company/create.html', title='Create Company', form=form)


@company_blueprint.route('/workplaces/<int:user_id>', methods=['GET', 'POST'])
@login_required
def workplace(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('company/workplace.html', title='Workplaces', user=user)


@company_blueprint.route('/profile/company_id/<int:company_id>', methods=['GET', 'POST'])
@login_required
def profile(company_id):
    company = Company.query.get_or_404(company_id)
    logo_file = url_for('static', filename='uploads/logo_img/' + company.logo_file)
    user = User.query.get_or_404(current_user.id)
    session['ORDERS_RCV'] = company.count_orders_received()
    print('Session Incoming_orders: ' + str(session['ORDERS_RCV']))
    return render_template('company/profile.html', title='Company Profile',
                                                    company=company,
                                                    logo_file=logo_file,
                                                    user=user)


@company_blueprint.route('/available_clinics')
@login_required
def available():
    companies = Company.query.all()
    return render_template('company/available_list.html', title='Available Clinics', companies=companies)


@company_blueprint.route('/teleconsult_queue/company_id/<int:company_id>', methods=['GET', 'POST'])
@login_required
def teleconsult_queue(company_id):
    company = Company.query.get_or_404(company_id)
    bookings_received = company.bookings_received.filter(Booking.consulted==False).order_by(Booking.timestamp.desc())
    bookings_accepted = current_user.bookings_accepted.order_by(Booking.timestamp.desc())
    return render_template('booking/dashboard.html', title='Teleconsult Queue', 
                                                            user=current_user, 
                                                            company=company,
                                                            bookings_received=bookings_received,
                                                            bookings_accepted=bookings_accepted)


@company_blueprint.route('/shop/company_id/<int:company_id>', methods=['GET', 'POST'])
@login_required
def shop(company_id):
    company = Company.query.get_or_404(company_id)
    return render_template('company/shop.html', title='Company Shop', company=company)


'''
@company_blueprint.route('/dashboard/company_id/<int:company_id>', methods=['GET', 'POST'])
@login_required
def dashboard(company_id):
    company = Company.query.get_or_404(company_id)
    return render_template('company/company_dashboard.html',
        title='Company Dashboard')
'''

@company_blueprint.route('/update/company_id/<int:company_id>', methods=['GET', 'POST'])
@login_required
def update(company_id):
    company = Company.query.get_or_404(company_id)
    form = UpdateCompanyForm()
    if form.validate_on_submit():
        company.name = form.name.data
        company.about_us = form.about_us.data
        company.building = form.building.data
        company.address = form.address.data
        company.unit_num = form.unit_num.data
        company.zip_code = form.zip_code.data
        company.country = form.country.data
        company.lat = form.lat.data
        company.lon = form.lon.data
        db.session.commit()

        # create first dataframe with dictionary
        df1 = pd.read_csv('companies.csv', header=0)
        for index, row in df1.iterrows():
            print(row['ID'], row['NAME'], row['LAT'], row['LON'])
            if str(row['ID']) == str(company.id):
                row['NAME'] = company.name
                row['LAT'] = company.lat
                row['LON'] = company.lon
        print(df1.at[0, 'NAME'])
        # create second dataframe with dictionary
        df2 = pd.DataFrame({
            'ID': [company.id],
            'NAME': [company.name],
            'LAT': [company.lat],
            'LON': [company.lon]})
        df1.update(df2)
        print(df2)
        df1.to_csv(r'companies.csv', index=False)

        flash('Company information updated.')
        return redirect(url_for('company.profile', company_id=company.id))

    elif request.method == 'GET':
        form.name.data = company.name
        form.about_us.data = company.about_us
        form.building.data = company.building
        form.address.data = company.address
        form.unit_num.data = company.unit_num
        form.zip_code.data = company.zip_code
        form.country.data = company.country
        form.lat.data = company.lat
        form.lon.data = company.lon
    return render_template('company/update.html', title='Edit Company', form=form, company=company)


@company_blueprint.route('/delete/company_id/<int:company_id>/user_id/<int:user_id>', methods=['GET', 'POST'])
@login_required
def delete(company_id, user_id):
    user = User.query.get_or_404(user_id)
    company = Company.query.get_or_404(company_id)
    db.session.delete(company)
    db.session.commit()
    flash('Company removed.')
    return redirect(url_for('company.workplace', user_id=user.id))


@company_blueprint.route('/add_employee/company_id/<int:company_id>', methods=['GET', 'POST'])
@login_required
def add_employee(company_id):
    company = Company.query.get_or_404(company_id)
    form = AddUserForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        company.employees.append(user)
        db.session.commit()
        flash('Employee added to Company')
        return redirect(url_for('company.profile', company_id=company.id))
    return render_template(
        'company/add_people.html', title='Add Employee', company=company, form=form)


@company_blueprint.route('/remove_employee/<int:user_id>/company_id/<int:company_id>', methods=['GET', 'POST'])
@login_required
def remove_employee(company_id, user_id):
    company = Company.query.get_or_404(company_id)
    user = User.query.get_or_404(user_id)
    company.employees.remove(user)
    db.session.commit()
    flash('Employee removed from Company')
    return redirect(url_for('company.profile', company_id=company.id))


@company_blueprint.route('/add_admin/company_id/<int:company_id>', methods=['GET', 'POST'])
@login_required
def add_admin(company_id):
    company = Company.query.get_or_404(company_id)
    form = AddUserForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        company.employees.append(user)
        company.administrators.append(user)
        db.session.commit()
        flash('Employee made Company administrator')
        return redirect(url_for('company.profile', company_id=company.id))
    return render_template(
        'company/add_people.html', title='Company Profile', company=company, form=form)


@company_blueprint.route('/remove_administrator/<int:user_id>/company_id/<int:company_id>', methods=['GET', 'POST'])
@login_required
def remove_admin(company_id, user_id):
    company = Company.query.get_or_404(company_id)
    user = User.query.get_or_404(user_id)
    company.administrators.remove(user)
    db.session.commit()
    flash('Company administrator removed from Company')
    return redirect(url_for('company.profile', company_id=company.id))


def save_photo(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.config['LOGO_IMG'], picture_fn)
    #picture_path = os.path.join(current_app.root_path, 'static/uploads/selfie_img', picture_fn)

    output_size = (250, 250)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@company_blueprint.route('/upload/company_id/<int:company_id>', methods=['GET', 'POST'])
@login_required
def upload(company_id):
    company = Company.query.get_or_404(company_id)
    form = UploadLogoForm()
    if form.validate_on_submit():
        if form.photo.data:
            photo_file = secure_filename(save_photo(form.photo.data))
            company.logo_file = photo_file
        db.session.commit()
        flash('Logo has been saved.')
        return redirect(url_for('company.profile',
            company_id=company.id))
    elif request.method == 'GET':
        #logo_file = url_for('static', filename='uploads/logo_img/' + company.logo_file)
        logo_file = url_for('company.get_logo', filename=company.logo_file)
    return render_template('user/upload_selfie.html', title='Upload Company Logo', logo_file=logo_file, form=form)


@company_blueprint.route('/get_logo/<filename>')
@login_required
def get_logo(filename):
    try:
        print(filename)
        return send_from_directory(os.path.join(current_app.config['LOGO_IMG']), filename)
    except FileNotFoundError:
        abort(404)
