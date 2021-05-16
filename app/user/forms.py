from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, IntegerField, FloatField, SelectField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, Optional

from app.user.models import User


class UpdateProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    designation = SelectField('Designation', validators=[Optional()],
                                                choices=[('Mr', 'Mr'),
                                                        ('Mrs', 'Mrs'),
                                                        ('Ms', 'Ms'),
                                                        ('Mdm', 'Mdm'),
                                                        ('Dr', 'Dr'),
                                                        ('Prof', 'Prof')])
    given_name = StringField('Given Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    nric = StringField('NRIC', validators=[DataRequired()])
    phone = StringField('Mobile Number', validators=[DataRequired()])
    about_me = TextAreaField('About Me (optional)', validators=[Optional()])
    building = StringField('Building Name (optional)', validators=[Optional()])
    address = StringField('Address (Enter only number)', validators=[Optional()])
    unit_num = StringField('Floor & Unit Number (optional)', validators=[Optional()])
    country = StringField('Country', validators=[Optional()])
    zip_code = IntegerField('Zip Code', validators=[Optional()])
    lat = FloatField('Latitude', validators=[Optional()])
    lon = FloatField('Longitude', validators=[Optional()])
    submit = SubmitField('Update')

    def __init__(self, original_username, original_email, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    # fix duplicate username bug
    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

    # fix duplicate email bug
    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=self.email.data).first()
            if user is not None:
                raise ValidationError('Please use a different email.')


class UpdateDoctorProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    designation = SelectField('Designation', validators=[Optional()],
                                                choices=[('Mr', 'Mr'),
                                                        ('Mrs', 'Mrs'),
                                                        ('Ms', 'Ms'),
                                                        ('Mdm', 'Mdm'),
                                                        ('Dr', 'Dr'),
                                                        ('Prof', 'Prof')])
    given_name = StringField('Given Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    nric = StringField('NRIC', validators=[DataRequired()])
    phone = StringField('Mobile Number', validators=[DataRequired()])
    about_me = TextAreaField('About Me (optional)', validators=[Optional()])
    building = StringField('Building Name (optional)', validators=[Optional()])
    address = StringField('Address', validators=[Optional()])
    unit_num = StringField('Floor & Unit Number (optional)', validators=[Optional()])
    country = StringField('Country', validators=[Optional()])
    zip_code = IntegerField('Zip Code', validators=[Optional()])
    lat = FloatField('Latitude', validators=[Optional()])
    lon = FloatField('Longitude', validators=[Optional()])
    practice = SelectField('Practice',
                        validators=[Optional()],
                        choices=[
                        ('General Practice', 'General Practice'),
                        ('Plastic Surgeon', 'Plastic Surgeon'),
                        ('Pediatrician', 'Pediatrician'),
                        ('Psychiatrist', 'Psychiatrist'),
                        ('Others', 'Others')])
    mreg_type = SelectField('Medical Registration Type', validators=[Optional()], 
                                                            choices=[('MCR', 'MCR'),
                                                                    ('Annual Practice Cert', 
                                                                    'Annual Practice Cert')])
    mreg = StringField('Medical Registration', validators=[DataRequired()])
    submit = SubmitField('Update')

    def __init__(self, original_username, original_email, *args, **kwargs):
        super(UpdateDoctorProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    # fix duplicate username bug
    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

    # fix duplicate email bug
    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=self.email.data).first()
            if user is not None:
                raise ValidationError('Please use a different email.')


class UploadSelfieForm(FlaskForm):
    photo = FileField('Upload Product Picture', validators=[FileAllowed(['jpeg', 'jpg', 'png'])])

