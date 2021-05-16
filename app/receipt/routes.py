from flask import flash, redirect, url_for
from flask_login import current_user, login_required

from app import db
from app.receipt import receipt_blueprint
from app.receipt.models import Receipt


@receipt_blueprint.route('/delete_receipt/<int:receipt_id>', methods=['GET', 'POST'])
@login_required
def delete(receipt_id):
	receipt = Receipt.query.get_or_404(receipt_id)
	db.session.delete(receipt)
	db.session.commit()
	flash('Receipt removed.')
	return redirect(url_for('cart.dashboard', cart_id=current_user.id))

# customer receipt generated from Booking.create route 
# provider receipt generated from Prescription.create