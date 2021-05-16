from flask import flash, render_template, request, redirect, url_for
from flask_login import current_user, login_required

from app import db
from app.currency import currency_blueprint
from app.currency.forms import CreateCurrencyForm, UpdateCurrencyForm
from app.currency.models import Currency


def check_superadmin():
    if not current_user.is_superadmin:
        abort(403)


@currency_blueprint.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    check_superadmin()

    form=CreateCurrencyForm() 
    if form.validate_on_submit(): 
        currency=Currency(
            name=form.name.data, 
            code=form.code.data, 
            unicode_decimal=form.unicode_decimal.data, 
            unicode_hex=form.unicode_hex.data, 
            sign=form.sign.data, 
            value=form.value.data, 
            format_str=form.format_str.data) 
        db.session.add(currency) 
        db.session.commit() 
        flash('currency created') 
        return redirect(url_for('admin.currency')) 
    return render_template('currency/create.html', title='Create Currency', form=form) 


@currency_blueprint.route('/update/<int:currency_id>', methods=['GET', 'POST'])
@login_required
def update(currency_id):
    check_superadmin()
    currency=Currency.query.get_or_404(currency_id)
    form=UpdateCurrencyForm()
    if form.validate_on_submit(): 
        currency.name=form.name.data 
        currency.code=form.code.data
        currency.unicode_decimal=form.unicode_decimal.data 
        currency.unicode_hex=form.unicode_hex.data 
        currency.sign=form.sign.data 
        currency.value=form.value.data 
        currency.format_str=form.format_str.data
        db.session.commit()
        flash('currency updated')
        return redirect(url_for('admin.currency'))
    elif request.method=='GET':
        form.name.data=currency.name 
        form.code.data=currency.code 
        form.unicode_decimal.data=currency.unicode_decimal 
        form.unicode_hex.data=currency.unicode_hex 
        form.sign.data=currency.sign 
        form.value.data=currency.value 
        form.format_str.data=currency.format_str 
    return render_template('currency/update.html', title='Edit Currency', form=form)


@currency_blueprint.route('/delete/<int:currency_id>', methods=['GET', 'POST'])
@login_required
def delete(currency_id):
    currency=Currency.query.get_or_404(currency_id)
    db.session.delete(currency)
    db.session.commit()
    flash('currency removed.')
    return redirect(url_for('admin.currency'))
