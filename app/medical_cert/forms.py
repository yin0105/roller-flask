from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.fields.html5 import IntegerField
from wtforms.validators import ValidationError, Optional

from app.medical_cert.models import MedicalCert

class CreateUnfitMedicalCertForm(FlaskForm): 
	num_of_unfit_days = IntegerField('Unfit for duties for how many days?', validators=[Optional()])
	submit = SubmitField('Submit')