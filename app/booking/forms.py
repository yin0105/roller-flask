from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Optional

from app.booking.models import Booking


class TelemedBookingForm(FlaskForm): 
	booking_type= SelectField('Type of Booking', 
		validators=[Optional()], 
		choices=[
		('Telemedicine', 'Telemedicine')])
	note = TextAreaField('Note (optional)', validators=[Optional()]) 
	submit = SubmitField('Create')
