from flask import Blueprint

feedback_blueprint = Blueprint('feedback', __name__, template_folder='templates')

from app.feedback import models