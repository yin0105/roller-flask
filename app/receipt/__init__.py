from flask import Blueprint

receipt_blueprint = Blueprint('receipt', __name__, template_folder='templates')

from app.receipt import routes, models

# customer receipt generated from Booking.create route 
# provider receipt generated from Prescription.create 