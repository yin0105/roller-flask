from flask import Blueprint

company_blueprint = Blueprint('company', __name__, template_folder='templates')

from app.company import routes, models