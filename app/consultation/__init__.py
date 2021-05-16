from flask import Blueprint

consultation_blueprint = Blueprint('consultation', __name__, template_folder='templates')

from app.consultation import routes, models