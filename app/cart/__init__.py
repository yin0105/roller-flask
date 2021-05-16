from flask import Blueprint

cart_blueprint = Blueprint('cart', __name__, template_folder='templates')

from app.cart import routes, models