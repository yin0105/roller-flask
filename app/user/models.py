import base64
import json
import os
import jwt

from datetime import datetime, timedelta
from time import time
from flask import current_app, url_for
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_

from app import db, login


class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data

companies_admins = db.Table('companies_admins',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('company_id', db.Integer, db.ForeignKey('company.id')))

workplaces_employees = db.Table('workplaces_employees',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('company_id', db.Integer, db.ForeignKey('company.id')))

consultations_providers = db.Table('consultations_providers',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('consultation_id', db.Integer, db.ForeignKey('consultation.id')))

deliveries_couriers = db.Table('deliveries_couriers',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('delivery_id', db.Integer, db.ForeignKey('delivery.id')))

class User(UserMixin, PaginatedAPIMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)

    password_hash = db.Column(db.String(128))
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    selfie_file = db.Column(db.String(128), nullable=False, default='default.jpg')
    designation = db.Column(db.String(32))
    given_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    nric = db.Column(db.String(64), index=True, unique=True)
    phone = db.Column(db.String(64))
    about_me = db.Column(db.String(1280))

    profession = db.Column(db.String(128))
    practice = db.Column(db.String(128))
    mreg_type = db.Column(db.String(64))
    mreg = db.Column(db.String(64), index=True, unique=True)

    is_doctor = db.Column(db.Boolean, default=False)
    is_courier = db.Column(db.Boolean, default=False)
    is_superadmin = db.Column(db.Boolean, default=False)

    building = db.Column (db.String(64))
    address = db.Column(db.String(128))
    unit_num = db.Column(db.String(32))
    country = db.Column (db.String(64))
    zip_code = db.Column(db.String(32))
    lat = db.Column(db.Float(precision=10, asdecimal=False, decimal_return_scale=None), nullable=True)
    lon = db.Column(db.Float(precision=10, asdecimal=False, decimal_return_scale=None), nullable=True)

    companies = db.relationship('Company',
        secondary=companies_admins, backref=db.backref('administrators', lazy='dynamic'))
    workplaces = db.relationship('Company',
        secondary=workplaces_employees, backref=db.backref('employees', lazy='dynamic'))

    health_record = db.relationship('HealthRecord', backref=db.backref('owner',
        lazy='joined', uselist=False, single_parent=True, cascade='all, delete-orphan'))

    cart = db.relationship('Cart', backref=db.backref('owner',
        lazy='joined', uselist=False, single_parent=True, cascade='all, delete-orphan'))
    orders = db.relationship('Order',
        foreign_keys='Order.buyer_id', backref='buyer', lazy='dynamic', cascade='all, delete-orphan')
    deliveries = db.relationship('Delivery',
        secondary=deliveries_couriers, backref=db.backref('couriers', lazy='dynamic'))

    bookings_sent = db.relationship('Booking',
        foreign_keys='Booking.customer_id', backref='customer', lazy='dynamic', cascade='all, delete')
    bookings_accepted = db.relationship('Booking',
        foreign_keys='Booking.provider_id', backref='provider', lazy='dynamic', cascade='all, delete')

    consultations = db.relationship('Consultation',
        secondary=consultations_providers, backref=db.backref('providers', lazy='dynamic'))
    consultations_provided = db.relationship('Consultation',
        foreign_keys='Consultation.primary_provider_id', backref='primary_provider', lazy='dynamic', cascade='all, delete')
    consultations_received = db.relationship('Consultation',
        foreign_keys='Consultation.customer_id', backref='customer', lazy='dynamic', cascade='all, delete')

    clinical_note_provided = db.relationship('ClinicalNote',
        foreign_keys='ClinicalNote.provider_id', backref='provider', lazy='dynamic', cascade='all, delete')
    clinical_note_received = db.relationship('ClinicalNote',
        foreign_keys='ClinicalNote.customer_id', backref='customer', lazy='dynamic', cascade='all, delete')
    medical_cert_provided = db.relationship('MedicalCert',
        foreign_keys='MedicalCert.provider_id', backref='provider', lazy='dynamic', cascade='all, delete')
    medical_cert_received = db.relationship('MedicalCert',
        foreign_keys='MedicalCert.customer_id', backref='customer', lazy='dynamic', cascade='all, delete')
    prescription_provided = db.relationship('Prescription',
        foreign_keys='Prescription.provider_id', backref='provider', lazy='dynamic', cascade='all, delete')
    prescription_received = db.relationship('Prescription',
        foreign_keys='Prescription.customer_id', backref='customer', lazy='dynamic', cascade='all, delete')
    customer_receipts = db.relationship('Receipt',
        foreign_keys='Receipt.customer_id', backref='customer', lazy='dynamic', cascade='all, delete')
    provider_receipts = db.relationship('Receipt',
        foreign_keys='Receipt.provider_id', backref='provider', lazy='dynamic', cascade='all, delete')

    messages_sent = db.relationship('Messages',
        foreign_keys='Messages.sender_id', backref='author', lazy='dynamic', cascade='all, delete')
    messages_received = db.relationship('Messages',
        foreign_keys='Messages.receiver_id', backref='recipient', lazy='dynamic', cascade='all, delete')
    notifications = db.relationship('Notification', backref='user', lazy='dynamic')

    created_on = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    online = db.Column(db.Boolean, default=False)

    # string method to print user
    def __str__(self):
        return f'User ID: {self.id, self.username}'

    def __repr__(self):
        return '<User {}>'.format(self.username, self.about_me)

    def mychats(self):
        from ..chat.models import Chats
        return Chats.query.filter(or_(Chats.user1 == self.id, Chats.user2 == self.id))

    def unread_chats(self):
        from ..chat.models import Messages
        return Messages.query.filter_by(recipient=self).filter(Messages.receiver_read==False).count()
        #return self.messages_received.filter_by(receiver_read=False).group_by(Messages.chat_id).count()

    def unread_msgs(self, chat_id):
        from ..chat.models import Messages
        return self.messages_received.filter_by(receiver_read=False, chat_id=chat_id).count()
        #return Messages.query.filter_by(recipient=self).filter_by(receiver_read=False, chat_id=chat_id).count()

    def add_notification(self, name, data):
        self.notifications.filter_by(name=name).delete()
        from ..chat.models import Notification #import Chat here to avoid circular dependency error
        n = Notification(name=name, payload_json=json.dumps(data), user=self)
        db.session.add(n)
        return n

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # jwt.encode
    def get_email_token(self, expires_in=99999):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    # jwt.decode
    @staticmethod
    def verify_email_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    # converting to dictionary data for api
    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'username': self.username, 
            'about_me': self.about_me,
            '_links': {
                'self': url_for('api.get_user', id=self.id),
            }
        }
        if include_email:
            data['email'] = self.email
        return data

    # converting to dictionary data for api
    def from_dict(self, data, new_user=False):
        for field in ['username', 'email', 'about_me']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

    # get token for api authentication
    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    # revoke token for api authentication
    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return 

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
