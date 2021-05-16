from flask import Blueprint

prescription_blueprint = Blueprint('prescription', __name__, template_folder='templates')

from app.prescription import routes, models