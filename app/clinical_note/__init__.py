from flask import Blueprint

clinical_note_blueprint = Blueprint('clinical_note', __name__, template_folder='templates')

from app.clinical_note import routes, models