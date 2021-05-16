from datetime import datetime
from flask import flash, render_template, redirect, url_for, \
    request, session
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user

from app import db
from app.auth import auth_blueprint
from app.auth.forms import LoginForm, RegistrationForm, \
    DoctorRegistrationForm, CourierRegistrationForm, FunnelRegistrationForm, \
    RegistrationNewsletterForm, ResetPasswordRequestForm, ResetPasswordForm
from app.email.lib import send_new_password_email, send_password_changed_email, \
    send_email_verification, send_email_newsletter_verification, send_email_newsletter_doctor_verification
from app.user.models import User
from app.cart.models import Cart
from app.health_record.models import HealthRecord
from app.currency.models import Currency


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user.dashboard', user_id=current_user.id))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('user.dashboard', user_id=current_user.id)
        return redirect(next_page)
    return render_template('auth/login.html', title='Login', form=form)


@auth_blueprint.route('/logout')
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect(url_for('home.index'))


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('user.dashboard', user_id=current_user.id))
    profession='Others'
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            profession=profession,
            email=form.email.data,
            confirmed=False)
        if user.email == 'kennethtangcn@gmail.com':
            user.is_superadmin=True
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.flush()
        cart = Cart(id=user.id, user_id=user.id)
        db.session.add(cart)
        health_record = HealthRecord(id=user.id, user_id=user.id)
        db.session.add(health_record)
        currencies = Currency.query.all()
        if Currency.currency_count() == 0:
            currency=Currency(name='Singapore Dollar', 
                                code='SGD',
                                sign='S$',
                                value=1, 
                                unicode_hex=24,
                                unicode_decimal=36)
            db.session.add(currency)
        db.session.commit()
        #send_email_verification(user) # email/lib.py
        flash('Please check your email to verify your registration. Thank you!')
        # get_email_token()
        return redirect(url_for('auth.login', token=user.get_email_token()))
    return render_template('auth/register.html', title='Register', form=form)


@auth_blueprint.route('/register/funnel', methods=['GET', 'POST'])
def register_funnel():
    if current_user.is_authenticated:
        return redirect(url_for('user.dashboard', user_id=current_user.id))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(profession='Others',
                    email=form.email.data,
                    confirmed=False)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.flush()
        cart = Cart(id=user.id, user_id=user.id)
        db.session.add(cart)
        health_record = HealthRecord(id=user.id, user_id=user.id)
        db.session.add(health_record)
        db.session.commit()
        #send_email_verification(user) # email/lib.py
        flash('Please check your email to verify your registration. Thank you!')
        # get_email_token()
        return redirect(url_for('auth.success'))
    return render_template('auth/register_funnel.html', title='Register', form=form)


@auth_blueprint.route('/register/funnel/success', methods=['GET', 'POST'])
def success():
    return render_template('auth/success.html', title='Registration Successful')


@auth_blueprint.route('/register/doctor', methods=['GET', 'POST'])
def register_doctor():
    if current_user.is_authenticated:
        return redirect(url_for('user.dashboard', user_id=current_user.id))
    form = DoctorRegistrationForm()
    if form.validate_on_submit():
        user = User(profession='Doctor',
                    email=form.email.data,
                    confirmed=False)
        user.is_doctor = True
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.flush()
        cart = Cart(id=user.id, user_id=user.id)
        db.session.add(cart)
        health_record = HealthRecord(id=user.id, user_id=user.id)
        db.session.add(health_record)
        db.session.commit()
        #send_email_verification(user) # email/lib.py
        flash('Please check your email to verify your registration. Thank you!')
        # get_email_token()
        return redirect(url_for('auth.login', token=user.get_email_token()))
    return render_template('auth/register_doctor.html', title='Doctor Registration', form=form)


@auth_blueprint.route('/register/courier', methods=['GET', 'POST'])
def register_courier():
    if current_user.is_authenticated:
        return redirect(url_for('user.dashboard', user_id=current_user.id))
    form = CourierRegistrationForm()
    if form.validate_on_submit():
        user = User(profession='Courier',
                    email=form.email.data,
                    confirmed=False)
        user.is_courier = True
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.flush()
        cart = Cart(id=user.id, user_id=user.id)
        db.session.add(cart)
        health_record = HealthRecord(id=user.id, user_id=user.id)
        db.session.add(health_record)
        db.session.commit()
        #send_email_verification(user) # email/lib.py
        flash('Please check your email to verify your registration. Thank you!')
        # get_email_token()
        return redirect(url_for('auth.login', token=user.get_email_token()))
    return render_template('auth/register.html', title='Register', form=form)


# when admin clicks on Email on admin.people dashboard (self-registered users)
@auth_blueprint.route('/send_email_verification/user_id/<int:user_id>', methods=['GET', 'POST'])
def send_verification_email(user_id):
    user = User.query.get_or_404(user_id)
    send_email_verification(user) # email/lib.py
    flash('Email verification sent')
    # get_email_token()
    return redirect(url_for('admin.people', token = user.get_email_token()))


# when user clicks on Verify my email password on verify_email.html (self-registered users)
@auth_blueprint.route('/verify_email/<token>', methods=['GET', 'POST'])
def verify_email(token):
    user = User.verify_email_token(token) # email/lib.py
    user.confirmed = True
    user.confirmed_on = datetime.utcnow()
    db.session.commit()
    flash('Thanks for verifying your email.')
    return redirect(url_for('home.index'))


'''
Admin-Registered Users
'''

# admin register on behalf of users
@auth_blueprint.route('/register/newsletter', methods=['GET', 'POST'])
def register_newsletter():
    form = RegistrationNewsletterForm()
    if form.validate_on_submit():
        user = User(profession='Others', 
                    username=form.username.data,
                    email=form.email.data,
                    confirmed=False)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.flush()
        cart = Cart(id=user.id, user_id=user.id)
        db.session.add(cart)
        health_record = HealthRecord(id=user.id, user_id=user.id)
        db.session.add(health_record)
        db.session.commit()
        send_email_newsletter_verification(user) # email/lib.py
        flash('User registered successfully.')
        # get_email_token()
        return redirect(url_for('auth.register_newsletter'))
    return render_template('auth/register_newsletter.html', title='Register', form=form)


# when admin clicks on Newsletter on admin.people dashboard (admin-registered users)
@auth_blueprint.route('/send_email/newsletter/verification/user_id/<int:user_id>', methods=['GET', 'POST'])
def send_newsletter_verification_email(user_id):
    user = User.query.get_or_404(user_id)
    send_email_newsletter_verification(user) # email/lib.py
    flash('Newsletter Email verification sent')
    # get_email_token()
    return redirect(url_for('admin.people', token = user.get_email_token()))


# when user clicks on Verify my email & change password on verify_newsletter_email.html (admin-registered users)
@auth_blueprint.route('/verify/newsletter/email/<token>', methods=['GET', 'POST'])
def verify_newsletter_email(token):
    user = User.verify_email_token(token)
    user.confirmed = True
    user.confirmed_on = datetime.utcnow()
    db.session.commit()
    flash('Thanks for verifying your email. Please change your password.')
    return redirect(url_for('auth.reset_newsletter_password', token = user.get_email_token()))


# redirected from auth.verify_newsletter_email (admin-registered users)
@auth_blueprint.route('/reset_newsletter_password/<token>', methods=['GET', 'POST'])
def reset_newsletter_password(token):
    user = User.verify_email_token(token) # email/lib.py
    if not user:
        return redirect(url_for('home.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        send_password_changed_email(user) # email/lib.py
        flash('Your password has been reset.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', title='Reset Password', form=form)


'''
Admin-Registered Doctors
'''

# admin register on behalf of doctors
@auth_blueprint.route('/register/newsletter/doctor', methods=['GET', 'POST'])
def register_newsletter_doctor():
    form = RegistrationNewsletterForm()
    if form.validate_on_submit():
        user = User(profession='Doctor', 
                    username=form.username.data, 
                    email=form.email.data, 
                    confirmed=False)
        user.is_doctor = True
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.flush()
        cart = Cart(id=user.id, user_id=user.id)
        db.session.add(cart)
        health_record = HealthRecord(id=user.id, user_id=user.id)
        db.session.add(health_record)
        db.session.commit()
        send_email_newsletter_doctor_verification(user) # email/lib.py
        flash('User registered successfully.')
        # get_email_token()
        return redirect(url_for('auth.register_newsletter_doctor'))
    return render_template('auth/register_newsletter_doctor.html', title='Register', form=form)


# when admin clicks on Newsletter on admin.doctor dashboard (admin-registered doctors)
@auth_blueprint.route('/send_email/doctor/newsletter/verification/user_id/<int:user_id>', methods=['GET', 'POST'])
def send_newsletter_doctor_verification_email(user_id):
    user = User.query.get_or_404(user_id)
    send_email_newsletter_doctor_verification(user) # email/lib.py
    flash('Newsletter Email verification sent')
    # get_email_token()
    return redirect(url_for('admin.people', token = user.get_email_token()))


# when doctor clicks on Verify my email & change password on verify_newsletter_doctor_email.html (admin-registered doctors)
@auth_blueprint.route('/verify/newsletter/doctor/email<token>', methods=['GET', 'POST'])
def verify_newsletter_doctor_email(token):
    user = User.verify_email_token(token) # email/lib.py
    user.confirmed = True
    user.confirmed_on = datetime.utcnow()
    db.session.commit()
    flash('Thanks for verifying your email. Please change your password.')
    return redirect(url_for('auth.reset_newsletter_password', token = user.get_email_token()))


# redirected from auth.verify_newsletter_doctor_email (admin-registered doctors)
@auth_blueprint.route('/reset_newsletter_password/<token>', methods=['GET', 'POST'])
def reset_newsletter_doctor_password(token):
    user = User.verify_email_token(token) # email/lib.py
    if not user:
        return redirect(url_for('home.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        send_password_changed_email(user) # email/lib.py
        flash('Your password has been reset.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', title='Reset Password', form=form)


''' 
REQUEST NEW PASSWORD
''' 

@auth_blueprint.route('/requesting_new_password', methods=['GET', 'POST'])
def requesting_new_password():
    if current_user.is_authenticated:
        return redirect(url_for('home.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            flash('Invalid email')
            return redirect(url_for('auth.reset_password_request'))
        if user:
            # send email credentials located in email/lib.py and .env files
            send_new_password_email(user)
        flash('Check your email for the instructions to reset your password')
        # token is defined in send_new_password_email helper method in app.email.lib.py
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html', title='Requesting Password Reset', form=form)


@auth_blueprint.route('/reset_password_request', methods=['GET', 'POST'])
def new_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('home.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            flash('Invalid email')
            return redirect(url_for('auth.reset_password_request'))
        if user:
            # send email credentials located in email/lib.py and .env files
            send_new_password_email(user)
        flash('Check your email for the instructions to reset your password')
        # token is defined in send_new_password_email helper method in app.email.lib.py
        return redirect(url_for('auth.reset_password', token = user.get_email_token()))
    return render_template('auth/reset_password_request.html', title='Reset Password Request', form=form)


@auth_blueprint.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('home.index'))
    user = User.verify_email_token(token)
    if not user:
        return redirect(url_for('home.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        send_password_changed_email(user)
        flash('Your password has been reset.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', title='Reset Password', form=form)
