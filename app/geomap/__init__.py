from flask import Blueprint

geomap_blueprint = Blueprint('geomap', __name__, template_folder='templates')

from app.geomap import routes