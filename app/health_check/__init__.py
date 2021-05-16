from flask import Blueprint

health_check_blueprint = Blueprint('health_check', __name__, template_folder='templates')

from app.health_check import routes