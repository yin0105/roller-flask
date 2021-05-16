from flask import render_template, request
from app import db
from app.alert import alert_blueprint


@alert_blueprint.app_errorhandler(403)
def forbidden_error(error):
    return render_template('error/403.html'), 403


@alert_blueprint.app_errorhandler(404)
def not_found_error(error):
	return render_template('error/404.html'), 404


@alert_blueprint.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('error/500.html'), 500

