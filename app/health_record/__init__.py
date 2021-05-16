from flask import Blueprint

health_record_blueprint = Blueprint('health_record', __name__, template_folder='templates')

from app.health_record import routes, models