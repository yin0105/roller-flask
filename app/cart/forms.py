from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired

from app.cart.models import Cart
from app.user.models import User


class CartForm(FlaskForm): 
    product = StringField('Product', validators=[DataRequired()])
    submit = SubmitField('Checkout')