from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, IntegerField, FloatField, SubmitField
from wtforms.validators import DataRequired, Optional, Length, Email

from app.company.models import Company


class CreateCompanyForm(FlaskForm):
    name = StringField('Company Name', validators=[DataRequired(), Length(min=0, max=256)])
    about_us = TextAreaField('About Us (optional)', validators=[Optional()])
    building = StringField('Building Name (optional)', validators=[Optional()])
    address = StringField('Address', validators=[DataRequired()])
    unit_num = StringField('Floor & Unit Number (optional)', validators=[Optional()])
    country = StringField('Country', validators=[DataRequired()])
    zip_code = IntegerField('Zip Code', validators=[DataRequired()])
    submit = SubmitField('Submit')


class UpdateCompanyForm(FlaskForm):
    name = StringField('Company Name', validators=[DataRequired(), Length(min=0, max=256)])
    about_us = TextAreaField('About Us (optional)', validators=[Optional()])
    building = StringField('Building Name (optional)', validators=[Optional()])
    address = StringField('Address', validators=[DataRequired()])
    unit_num = StringField('Floor & Unit Number (optional)', validators=[Optional()])
    country = StringField('Country', validators=[DataRequired()])
    zip_code = IntegerField('Zip Code', validators=[DataRequired()])
    lat = FloatField('Latitude', validators=[Optional()])
    lon = FloatField('Longitude', validators=[Optional()])
    submit = SubmitField('Submit')


class AddUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Add User')


class UploadLogoForm(FlaskForm):
    photo = FileField('Upload Product Picture', validators=[FileAllowed(['jpeg', 'jpg', 'png'])])