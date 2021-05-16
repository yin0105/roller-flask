from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired

from app.receipt.models import Receipt
from app.currency.models import Currency


class CreateReceiptForm(FlaskForm): 
    description = TextAreaField('Description', validators=[DataRequired()])
    currency = SelectField('Currency', validators=[DataRequired()])
    price_amount = StringField('Price', validators=[DataRequired()])
    discount_amount = StringField('Discount', validators=[DataRequired()])
    service_amount = StringField('Service Fee', validators=[DataRequired()])
    customer_paid_amount = StringField('Customer Pays', validators=[DataRequired()])
    provider_received_amount = StringField('Pay Provider', validators=[DataRequired()])
    submit = SubmitField('Create')

    def __init__(self, *args, **kwargs):
        super(CreateReceiptForm, self).__init__(*args, **kwargs)
        self.currency.choices = [(c.code, c.code) for c in Currency.query.order_by(Currency.code)]


class UpdateReceiptForm(FlaskForm): 
    description = TextAreaField('Description', validators=[DataRequired()])
    currency = SelectField('Currency', validators=[DataRequired()])
    price_amount = StringField('Price', validators=[DataRequired()])
    discount_amount = StringField('Discount', validators=[DataRequired()])
    service_amount = StringField('Service Fee', validators=[DataRequired()])
    customer_paid_amount = StringField('Customer Pays', validators=[DataRequired()])
    provider_received_amount = StringField('Pay Provider', validators=[DataRequired()])

    submit = SubmitField('Update')

    def __init__(self, *args, **kwargs):
        super(UpdateReceiptForm, self).__init__(*args, **kwargs)
        self.currency.choices = [(c.code, c.code) for c in Currency.query.order_by(Currency.code)]