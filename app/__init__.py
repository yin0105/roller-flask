import os
import arrow
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_socketio import SocketIO

from config import Config
from lib.money import *


naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
    }


#db = SQLAlchemy()
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()
bootstrap = Bootstrap()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = '你好! Please log in to access this page.'
mail = Mail()
moment = Moment()
socketio = SocketIO()


def create_app():
	app = Flask(__name__, static_url_path='/static')
	app.config.from_object(Config)

	db.init_app(app)
	#migrate.init_app(app, db)
	migrate.init_app(app, db, render_as_batch=True) 
	bootstrap.init_app(app)
	login.init_app(app) #see user.model from app import login
	mail.init_app(app)
	moment.init_app(app)
	socketio.init_app(app) 

	from app.admin import admin_blueprint
	app.register_blueprint(admin_blueprint, url_prefix='/admin')

	from app.alert import alert_blueprint
	app.register_blueprint(alert_blueprint)

	from app.api import api_blueprint
	app.register_blueprint(api_blueprint, url_prefix='/api')

	from app.auth import auth_blueprint
	app.register_blueprint(auth_blueprint, url_prefix='/auth')

	from app.base import base_blueprint
	app.register_blueprint(base_blueprint)

	from app.billing import billing_blueprint
	app.register_blueprint(billing_blueprint)

	from app.billing_consult import billing_consult_blueprint
	app.register_blueprint(billing_consult_blueprint)

	from app.booking import booking_blueprint
	app.register_blueprint(booking_blueprint, url_prefix='/booking_dashboard')

	from app.cart import cart_blueprint
	app.register_blueprint(cart_blueprint, url_prefix='/cart')

	from app.chat import chat_blueprint
	app.register_blueprint(chat_blueprint, url_prefix='/chat')

	from app.clinical_note import clinical_note_blueprint
	app.register_blueprint(clinical_note_blueprint, url_prefix='/clinical_note')

	from app.construction import construction_blueprint
	app.register_blueprint(construction_blueprint)

	from app.consultation import consultation_blueprint
	app.register_blueprint(consultation_blueprint, url_prefix='/consultation')

	from app.company import company_blueprint
	app.register_blueprint(company_blueprint, url_prefix='/company')

	from app.currency import currency_blueprint
	app.register_blueprint(currency_blueprint)

	from app.delivery import delivery_blueprint
	app.register_blueprint(delivery_blueprint, url_prefix='/delivery')

	from app.email import email_blueprint
	app.register_blueprint(email_blueprint)

	from app.feedback import feedback_blueprint
	app.register_blueprint(feedback_blueprint)

	from app.geomap import geomap_blueprint
	app.register_blueprint(geomap_blueprint, url_prefix='/geomap')

	from app.health_check import health_check_blueprint
	app.register_blueprint(health_check_blueprint, url_prefix='/health_check')

	from app.health_record import health_record_blueprint
	app.register_blueprint(health_record_blueprint, url_prefix='/health_record')

	from app.home import home_blueprint
	app.register_blueprint(home_blueprint)

	from app.order import order_blueprint
	app.register_blueprint(order_blueprint, url_prefix='/order')

	from app.medical_cert import medical_cert_blueprint
	app.register_blueprint(medical_cert_blueprint)

	from app.prescription import prescription_blueprint
	app.register_blueprint(prescription_blueprint)

	from app.product import product_blueprint
	app.register_blueprint(product_blueprint, url_prefix='/product')

	from app.receipt import receipt_blueprint
	app.register_blueprint(receipt_blueprint, url_prefix='/receipt')

	from app.user import user_blueprint
	app.register_blueprint(user_blueprint, url_prefix='/user')


	def datetimeformat(date_str):
		dt = arrow.get(date_str)
		return dt.humanize()
	app.jinja_env.filters['datetimeformat'] = datetimeformat

	def format_amount(amount, convert_to_dollars=True):
		if convert_to_dollars:
			amount = cents_to_dollars(amount)
		return '{:,.2f}'.format(amount)
	app.jinja_env.filters['format_amount'] = format_amount

	def format_stripe_amount(amount):
		amount = amount * 100
		return amount
	app.jinja_env.filters['format_stripe_amount'] = format_stripe_amount

	'''
	if not app.debug and not app.testing:
		# email error log
		if app.config['MAIL_SERVER']:
			auth = None
			if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
				auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
			secure = None
			if app.config['MAIL_USE_TLS']:
				secure = ()
			mail_handler = SMTPHandler(
				mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
				fromaddr='no-reply@' + app.config['MAIL_SERVER'],
				toaddrs=app.config['ADMINS'], subject='Application Failure',
				credentials=auth, secure=secure)
			mail_handler.setLevel(logging.ERROR)
			app.logger.addHandler(mail_handler)

		# error log to file
		if not os.path.exists('logs'):
			os.mkdir('logs')
		file_handler = RotatingFileHandler('logs/zoz.log', maxBytes=10240, backupCount=10)
		file_handler.setFormatter(logging.Formatter(
			'%(asctime)s %(levelname)s: %(message)s '
			'[in %(pathname)s:%(lineno)d]'))
		file_handler.setLevel(logging.INFO)
		app.logger.addHandler(file_handler)

		app.logger.setLevel(logging.INFO)
		app.logger.info('Application startup')
	'''

	return app
