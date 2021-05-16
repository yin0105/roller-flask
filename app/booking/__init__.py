from flask import Blueprint

booking_blueprint = Blueprint('booking', __name__, template_folder='templates')

from app.booking import routes, models