from flask import Blueprint

billing_blueprint = Blueprint('billing', __name__, template_folder='templates')

from app.billing import routes