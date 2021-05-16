import os
import stripe
import functools

from flask import flash, render_template, request, redirect, url_for, session, jsonify, abort
from flask_login import current_user, login_required
from sqlalchemy.orm import aliased
from flask_socketio import SocketIO, send, emit
from .. import socketio

from app import db
from app.cart import cart_blueprint
from app.cart.models import Cart, CartItem
from app.order.models import Order
from app.user.models import User
from app.company.models import Company
from app.product.models import Product


stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
checkout_public_key = os.environ.get('STRIPE_PUBLIC_KEY')
endpoint_secret = os.environ.get('STRIPE_END_POINT_SECRET')


def check_superadmin():
    if not current_user.is_superadmin:
        abort(403)


@cart_blueprint.route('/create_cart/user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def create(user_id):
    user = User.query.get_or_404(current_user.id)
    if request.method == 'POST':
        if cart == '':
            cart = Cart(id=current_user.id, user_id=current_user.id)
            db.session.add(cart)
            db.session.commit()
            flash('Shopping cart created.')
            return redirect(url_for('cart.dashboard', user=user))


@cart_blueprint.route('/dashboard/<int:cart_id>', methods=['GET', 'POST'])
@login_required
def dashboard(cart_id):
    user = User.query.get_or_404(current_user.id)
    cart = Cart.query.get_or_404(cart_id)
    currency = cart.get_currency()
    total_items = cart.count_total_items()
    total_amount = cart.count_total_amount()

    session['CART'] = cart.count_total_items()
    print('Session Cart Items: ' + str(session['CART']))

    orders = Order.query.join(Order.buyer).filter(User.id==user.id)
    session['ORDER'] = orders.count()
    
    return render_template('cart/dashboard.html', 
        title='Cart', 
        user=user, 
        cart=cart,
        currency=currency, 
        total_items=total_items, 
        total_amount=total_amount, 
        orders = orders, 
        checkout_public_key=checkout_public_key)


@cart_blueprint.route('/delete_cart/<int:cart_id>/<int:user_id>', methods=['GET', 'POST'])
@login_required
def delete(cart_id, user_id):
    check_superadmin()
    cart = Cart.query.get_or_404(cart_id)
    user_id = cart_id
    db.session.delete(cart)
    db.session.commit()
    return redirect(url_for('admin.cart'))


@cart_blueprint.route('/add_item/<int:product_id>', methods=['GET', 'POST'])
@login_required
def add_item(product_id):
    product = Product.query.get_or_404(product_id)

    company_id = product.company_id
    supplier = Company.query.get_or_404(company_id)

    cart_id = current_user.id
    cart = Cart.query.get(int(cart_id))
    
    if any(product.id==cart_item.product_id for cart_item in cart.cart_items):
        cart_item = CartItem.query.filter(CartItem.product_id==product_id).\
                                    join(CartItem.cart).\
                                    filter(Cart.id==cart_id).first()
        print(f'CartItem ID: {cart_item.id} instantiated')
        
        cart_item.quantity += 1
        quantity = cart_item.quantity
        print(f'CartItem ID: {cart_item.id} quantity incremented')

        #Calculations for total amount of each item
        cart_item.ttl_amount = (quantity * cart_item.amount)
        ttl_amount = cart_item.ttl_amount
        print(f'CartItem ID: {cart_item.id} ttl_amount incremented')

        cart_item = CartItem(id=cart_item.id, quantity=quantity, ttl_amount=ttl_amount)
        print(f'CartItem ID: {cart_item.id} updating')
        db.session.commit()

        print(f'CartItem ID: {cart_item.id} committed')
        flash(f'CartItem ID: {cart_item.id} is in the cart. Quantity and total amount adjusted.')
    else:
        ttl_amount = product.amount

        cart_item = CartItem(product_id=product.id, 
                            supplier=supplier, 
                            brand=product.brand, 
                            model=product.model, 
                            currency=product.currency, 
                            amount=product.amount, 
                            quantity=1, 
                            ttl_amount=ttl_amount, 
                            feature_picture=product.feature_picture, 
                            cart_id=cart_id)
        db.session.add(cart_item)
        cart.cart_items.append(cart_item)
        db.session.commit()
        flash(f'CartItem ID: {cart_item.id} added to cart')
    return redirect(url_for('product.profile', product_id=product.id, cart_id=cart_id, cart=cart, cart_item=cart_item))


@cart_blueprint.route('/remove_item/<int:cart_item_id>', methods=['GET', 'POST'])
@login_required
def remove_item(cart_item_id):
    #cart_id = current_user.id
    cart_item = CartItem.query.get_or_404(cart_item_id)
    cart_id = cart_item.cart_id
    cart = Cart.query.get(int(cart_id))
    cart.cart_items.remove(cart_item)
    db.session.commit()
    print(f'CartItem ID: {cart_item.id} removed from cart')
    flash(f'CartItem ID: {cart_item.id} removed from cart')
    return redirect(url_for('cart.dashboard', cart_id=cart_id, cart=cart, cart_item=cart_item))
