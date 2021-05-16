from flask import flash, render_template
from app.base import base_blueprint


@base_blueprint.route('/faq')
def faq():
    return render_template('footer/faq.html', title='FAQ')


@base_blueprint.route('/policy_privacy')
def privacy_policy():
	return render_template('footer/privacy_policy.html', title='Privacy Policy')


@base_blueprint.route('/policy_refund')
def refund_policy():
	return render_template('footer/refund_policy.html', title='Refund Policy')


@base_blueprint.route('/use_terms')
def use_terms():
	return render_template('footer/use_terms.html', title='Use Terms')
