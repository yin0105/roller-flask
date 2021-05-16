from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired

from app.product.models import Product
from app.currency.models import Currency


class CreateProductForm(FlaskForm): 
    brand = StringField('Brand', validators=[DataRequired()])
    model = StringField('Model', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    currency = SelectField('Currency', validators=[DataRequired()])
    amount = StringField('Amount', validators=[DataRequired()])
    quantity = StringField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Create')

    def __init__(self, *args, **kwargs):
        super(CreateProductForm, self).__init__(*args, **kwargs)
        self.currency.choices = [(c.code, c.code) for c in Currency.query.order_by(Currency.code)]


class UpdateProductForm(FlaskForm): 
    brand = StringField('Brand', validators=[DataRequired()])
    model = StringField('Model', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    currency = SelectField('Currency', validators=[DataRequired()])
    amount = StringField('Amount', validators=[DataRequired()])
    quantity = StringField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Update')

    def __init__(self, *args, **kwargs):
        super(UpdateProductForm, self).__init__(*args, **kwargs)
        self.currency.choices = [(c.code, c.code) for c in Currency.query.order_by(Currency.code)]


class UploadImgForm(FlaskForm):
    photo = FileField('Upload Product Picture', validators=[FileAllowed(['jpeg', 'jpg', 'png'])])
