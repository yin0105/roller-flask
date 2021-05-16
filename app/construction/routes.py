from flask import flash, render_template


from app.construction import construction_blueprint


@construction_blueprint.route('/under_construction')
def landing():
	return render_template('construction/under_construction.html', title='Under Construction')
