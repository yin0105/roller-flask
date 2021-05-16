from flask import Blueprint

construction_blueprint = Blueprint('construction', __name__, template_folder='templates')

from app.construction import routes