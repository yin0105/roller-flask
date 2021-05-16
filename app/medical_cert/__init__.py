from flask import Blueprint

medical_cert_blueprint = Blueprint('medical_cert', __name__, template_folder='templates')

from app.medical_cert import routes, models