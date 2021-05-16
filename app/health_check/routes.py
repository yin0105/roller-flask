from flask import flash, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from datetime import datetime

from app import db
from app.health_check import health_check_blueprint
from app.user.models import User
from app.receipt.models import Receipt


@health_check_blueprint.route('/user_id/<int:user_id>', methods=['GET', 'POST'])
@login_required
def check_list(user_id):
	customer = User.query.get_or_404(user_id)
	if customer.phone != None:
		return render_template('health_check/checklist.html', title='Consulting', 
																customer=customer)
	elif customer.phone == None:
		return redirect(url_for('user.update', user_id=current_user.id, 
											username=current_user.username))
