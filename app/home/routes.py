import os
from datetime import datetime, date
import calendar
from flask import flash, render_template, redirect, url_for, session
from flask_login import current_user

from app import db
from app.home import home_blueprint
from app.feedback.models import Feedback
from app.feedback.forms import FeedbackForm
from app.product.models import Product
from app.user.models import User


@home_blueprint.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@home_blueprint.route('/')
@home_blueprint.route('/home', methods=['GET', 'POST'])
def index():
    users = User.query.order_by(User.created_on.desc()).all()
    products = Product.query.order_by(Product.created_on.desc()).all()
    form=FeedbackForm()
    if form.validate_on_submit(): 
        feedback=Feedback(
            username=form.username.data, 
            email=form.email.data, 
            body=form.body.data) 
        db.session.add(feedback) 
        db.session.commit() 
        flash('Thanks for your feedback.') 
        return redirect(url_for('home.index'))
    return render_template('home/index.html', title='Home', 
                                                users=users, 
                                                products=products, 
                                                form=form)


@home_blueprint.route('/')
@home_blueprint.route('/feedback', methods=['GET', 'POST'])
def feedback():
    form=FeedbackForm()
    if form.validate_on_submit(): 
        feedback=Feedback(
            username=form.username.data, 
            email=form.email.data, 
            body=form.body.data) 
        db.session.add(feedback) 
        db.session.commit() 
        flash('Thanks for your feedback.') 
        return redirect(url_for('home.index'))
    return render_template('feedback/wall.html', title='Feedback', form=form)
