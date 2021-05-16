from flask import flash, render_template, redirect, url_for
from flask_login import current_user, login_required, current_user
from datetime import datetime

from app import db
from app.health_record import health_record_blueprint
from app.health_record.models import HealthRecord
from app.clinical_note.models import ClinicalNote
from app.consultation.models import Consultation
from app.user.models import User


@health_record_blueprint.route('/<int:health_record_id>/user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def show(health_record_id, user_id):
	user = User.query.filter(User.id == int(user_id)).first_or_404()
	health_record_id = user.id
	health_record = HealthRecord.query.get_or_404(health_record_id)
	consultations = Consultation.query.all()
	consultations_received = user.consultations_received.order_by(Consultation.created_on.desc())
	print(f'{consultations_received}')
	consultations_provided = user.consultations_provided.order_by(Consultation.created_on.desc())
	return render_template('health_record/health_record.html', 
							title='Health Dashboard', 
							user=user, 
							health_record=health_record,
							consultations_received=consultations_received, 
							consultations_provided=consultations_provided,
							consultations=consultations)
