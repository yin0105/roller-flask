from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import ValidationError, Optional
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from app.prescription.models import Prescription
from app.product.models import Product, get_product


class PrescriptionForm(FlaskForm):
	product = QuerySelectField('Select Product', query_factory=get_product, get_label='model')
	body = TextAreaField('Prescription', validators=[Optional()])
	submit = SubmitField('Submit')

class AddProductForm(FlaskForm):
	product = QuerySelectField('Select Product', query_factory=lambda: Product.query.all())