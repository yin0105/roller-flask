from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from app.currency.models import Currency

class CreateCurrencyForm(FlaskForm): 
    name = StringField('Name', validators=[DataRequired()]) 
    code = StringField('Code', validators=[DataRequired()]) 
    unicode_decimal = StringField('Unicode_Decimal', validators=[DataRequired()]) 
    unicode_hex = StringField('Unicode_Hex', validators=[DataRequired()]) 
    sign = StringField('Sign', validators=[DataRequired()]) 
    value = StringField('Value', validators=[DataRequired()]) 
    format_str = StringField('Format String', validators=[DataRequired()]) 
    submit = SubmitField('Create')


class UpdateCurrencyForm(FlaskForm): 
    name = StringField('Name', validators=[DataRequired()]) 
    code = StringField('Code', validators=[DataRequired()]) 
    unicode_decimal = StringField('Unicode_Decimal', validators=[DataRequired()]) 
    unicode_hex = StringField('Unicode_Hex', validators=[DataRequired()]) 
    sign = StringField('Sign', validators=[DataRequired()]) 
    value = StringField('Value', validators=[DataRequired()]) 
    format_str = StringField('Format String', validators=[DataRequired()]) 
    submit = SubmitField('Update')

