import base64
import json
from datetime import datetime
from time import time

from app import db


class Chats(db.Model):
    __tablename__ = 'chats'
    id = db.Column(db.Integer, primary_key=True)
    user1 = db.Column(db.Integer, index=True)
    user2 = db.Column(db.Integer, index=True)
    msgs = db.relationship('Messages', 
        foreign_keys='Messages.chat_id', backref='chat_session', lazy='dynamic', cascade='all, delete')

    def __repr__(self):
        return '<Chat between {} and {}>'.format(self.user1, self.user2)
    
    def last_msg(self):
        return Messages.query.filter_by(chat_id=self.id).order_by(Messages.timestamp.desc()).first()

    def other(self,this_user_id):
        from app.user.models import User
        if this_user_id == self.user1:
            return User.query.get(self.user2)
        elif this_user_id == self.user2:
            return User.query.get(self.user1)


class Messages(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver_read = db.Column(db.Boolean, default=False)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    chat_id = db.Column(db.Integer, db.ForeignKey('chats.id'))

    def __repr__(self):
        return '<Messages {}>'.format(self.body)


class Notification(db.Model):
    __tablename__ = 'notification'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.Float, index=True, default=time)
    payload_json = db.Column(db.Text)

    def get_data(self):
        return json.loads(str(self.payload_json))

