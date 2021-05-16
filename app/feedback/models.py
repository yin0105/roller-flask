from datetime import datetime

from app import db

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    email = db.Column(db.String(128), index=True)
    body = db.Column(db.String(960))
    created_on = db.Column(db.DateTime, index=True, default=datetime.utcnow)