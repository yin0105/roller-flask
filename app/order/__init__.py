from flask import Blueprint

order_blueprint = Blueprint('order', __name__, template_folder='templates')

from app.order import routes, models