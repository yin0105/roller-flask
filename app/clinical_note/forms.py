from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import ValidationError, Optional

from app.clinical_note.models import ClinicalNote

class CreateClinicalNoteForm(FlaskForm):
	body = TextAreaField('Clinical Note', validators=[Optional()]) 
	submit = SubmitField('Submit')