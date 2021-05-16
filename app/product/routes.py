from flask import flash, render_template, request, redirect, url_for, \
    current_app, send_from_directory, abort, session
from werkzeug.utils import secure_filename 
from flask_login import current_user, login_required

import os
import secrets
from PIL import Image

from app import db
from app.product import product_blueprint
from app.product.forms import CreateProductForm, UpdateProductForm, UploadImgForm
from app.product.models import Product, Picture
from app.cart.models import Cart, CartItem
from app.company.models import Company


@product_blueprint.route('/create/company_id/<int:company_id>', methods=['GET', 'POST'])
@login_required
def create(company_id):
    company = Company.query.get_or_404(company_id)
    form=CreateProductForm()
    if form.validate_on_submit():
        dollar = form.amount.data
        amount = int(dollar)
        product=Product(
            brand=form.brand.data,
            model=form.model.data,
            description=form.description.data,
            currency=form.currency.data,
            amount=amount,
            quantity=form.quantity.data,
            company_id=company_id)
        db.session.add(product)
        company.products.append(product)
        db.session.commit()
        flash('Product created')
        return redirect(url_for('company.shop', company_id=company.id))
    return render_template('product/create.html', title='Create Product', form=form)


@product_blueprint.route('/marketplace')
@login_required
def marketplace():
    products = Product.query.order_by(Product.created_on.desc()).all()
    return render_template('product/marketplace.html', title='Showroom', products=products)


@product_blueprint.route('/profile/product_id/<int:product_id>')
@login_required
def profile(product_id):
    product = Product.query.get_or_404(product_id)
    company_id = product.company_id
    company = Company.query.get_or_404(company_id)
    #update cart_item number when product is added to cart
    cart_id = current_user.id
    cart = Cart.query.get_or_404(cart_id)
    session['CART'] = cart.count_total_items()
    print('Session Cart Items: ' + str(session['CART']))
    return render_template('product/profile.html', title='Product', product=product, company=company)


@product_blueprint.route('/update/<int:product_id>', methods=['GET', 'POST'])
@login_required
def update(product_id):
    product = Product.query.get_or_404(product_id)
    company = Company.query.get_or_404(product.company_id)
    form = UpdateProductForm()
    if form.validate_on_submit(): 
        product.brand = form.brand.data 
        product.model = form.model.data 
        product.description = form.description.data 
        product.currency = form.currency.data 
        product.amount = form.amount.data
        product.quantity = form.quantity.data
        db.session.commit() 
        flash('Product information updated.')
        return redirect(url_for('company.shop', company_id=company.id))
        #return redirect(url_for('product.profile', product_id=product.id))
    elif request.method == 'GET':
        form.brand.data = product.brand
        form.model.data = product.model 
        form.description.data = product.description
        form.currency.data = product.currency
        form.amount.data = product.amount
        form.quantity.data = product.quantity
    return render_template('product/update.html', title='Edit Product', form=form)


@product_blueprint.route('/delete/<int:product_id>', methods=['GET', 'POST'])
@login_required
def delete(product_id):
    product = Product.query.get_or_404(product_id)
    company = product.supplier
    db.session.delete(product)
    db.session.commit()
    flash('Product removed.')
    return redirect(url_for('company.shop', company_id=company.id))


def save_photo(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + f_ext
    picture_path = os.path.join(current_app.config['PRODUCT_IMG'], picture_filename)
    #picture_path = os.path.join(current_app.root_path, 'static/uploads/product_img', picture_filename)

    output_size = (250, 250)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_filename


@product_blueprint.route('/upload/<int:product_id>', methods=['GET', 'POST'])
@login_required
def upload(product_id):
    product = Product.query.get_or_404(product_id)
    company = product.supplier
    form = UploadImgForm()
    if form.validate_on_submit():
        photo_file = secure_filename(save_photo(form.photo.data))
        product.feature_picture = photo_file
        picture = Picture(picture_file=photo_file, product_id=product.id) 
        product.pictures.append(picture)
        db.session.commit()
        flash('Product image uploaded.')
        return redirect(url_for('company.shop', company_id=company.id))
        #return redirect(url_for('product.profile', product_id=product.id))
    return render_template('product/upload_img.html', title='Upload Product Image', form=form)


@product_blueprint.route('/get_featured/<filename>')
@login_required
def get_featured(filename):
    try:
        print(filename)
        return send_from_directory(os.path.join(current_app.config['PRODUCT_IMG']), filename)
    except FileNotFoundError:
        abort(404)


@product_blueprint.route('/get_image/<picture_id>/<filename>')
@login_required
def get_image(picture_id, filename):
    picture = Picture.query.get_or_404(picture_id)
    filename = picture.picture_file
    try:
        print(filename)
        return send_from_directory(os.path.join(current_app.config['PRODUCT_IMG']), filename)
    except FileNotFoundError:
        abort(404)


@product_blueprint.route('/delete_image/<int:product_id>/<int:picture_id>/<filename>')
@login_required
def delete_image(product_id, picture_id, filename):
    product = Product.query.get_or_404(product_id)
    picture = Picture.query.get_or_404(picture_id)
    filename = picture.picture_file
    product.pictures.remove(picture)
    db.session.commit()
    flash('Image removed.')
    return redirect(url_for('product.profile', product_id=product.id))
