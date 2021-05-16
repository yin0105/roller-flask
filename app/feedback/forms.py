from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email

from app.feedback.models import Feedback


class FeedbackForm(FlaskForm):
	username = StringField('Name', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	body = TextAreaField('Message', validators=[DataRequired()])