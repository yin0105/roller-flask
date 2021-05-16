from flask import Blueprint

billing_consult_blueprint = Blueprint('billing_consult', __name__, template_folder='templates')

from app.billing_consult import routes