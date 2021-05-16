from flask import Blueprint

delivery_blueprint = Blueprint('delivery', __name__, template_folder='templates')

from app.delivery import routes, models