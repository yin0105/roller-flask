from flask import Blueprint

base_blueprint = Blueprint('base', __name__, template_folder='templates')

from app.base import routes