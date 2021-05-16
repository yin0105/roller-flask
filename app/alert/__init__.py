from flask import Blueprint

alert_blueprint = Blueprint('alert', __name__, template_folder='templates')

from app.alert import handlers