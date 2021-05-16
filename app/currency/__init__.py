from flask import Blueprint

currency_blueprint = Blueprint('currency', __name__, template_folder='templates')

from app.currency import routes