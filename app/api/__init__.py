from flask import Blueprint

api_blueprint = Blueprint('api', __name__, template_folder='templates')

from app.api import users, errors, tokens