import os
import stripe
import functools

from flask import flash, render_template, request, redirect, url_for, \
    session, jsonify, abort
from flask_login import current_user, login_required

from app import db
from app.billing_consult import billing_consult_blueprint
from app.user.models import User
from app.cart.models import Cart, CartItem
from app.company.models import Company
from app.product.models import Product
from app.order.models import Order, IncomingOrder


stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
checkout_public_key = os.environ.get('STRIPE_PUBLIC_KEY')
endpoint_secret = os.environ.get('STRIPE_END_POINT_SECRET')


@billing_consult_blueprint.route('/create-checkout-session', methods=['POST'])
@login_required
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'sgd',
                        'unit_amount': 1800,
                        'product_data': {
                            'name': 'Tele-Health Consultation',
                            'images': ['https://i.imgur.com/EHyR2nP.png'],
                        },
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=url_for('billing_consult.success', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=url_for('home.index', _external=True),
        )
        return jsonify({'id': checkout_session.id})
    except Exception as e:
        return jsonify(error=str(e)), 403


@billing_consult_blueprint.route('/successful/2', methods=['GET', 'POST'])
@login_required
def success():
    '''
    cart_id = current_user.id
    cart = Cart.query.get_or_404(cart_id)
    buyer_id = current_user.id
    order = Order(buyer_id=buyer_id)
    order.cart_items.extend(cart.cart_items) #copy cart.cart_items to order.cart_items
    db.session.add(order)
    db.session.flush()

    for cart_item in cart.cart_items:
        cart_item.cart_id = None #remove cart_item from cart
        company = cart_item.supplier
        company.orders.append(order)

        if any(cart_item.supplier_id==company.id for cart_item in order.cart_items):
            incoming_order = IncomingOrder(order_id=order.id, company_id=company.id)
            db.session.add(incoming_order)
            company.incoming_orders.append(incoming_order)
            cart_items = CartItem.query.filter(CartItem.order_id==order.id).\
                            filter(CartItem.supplier==company).all()
            for cart_item in cart_items:
                incoming_order.cart_items.append(cart_item)

    db.session.commit()

    session['CART'] = cart.count_total_items()
    print('Session Cart Items: ' + str(session['CART']))

    orders = Order.query.join(Order.buyer).filter(User.id==current_user.id)
    session['ORDER'] = orders.count()
    '''
    return redirect(url_for('company.available'))
    #return render_template('billing_consult/success.html', title='Payment Successful')


@billing_consult_blueprint.route('/stripe_webhook', methods=['POST'])
@login_required
def stripe_webhook():
    print('Webhook called.')
    # abort if user sends data larger than 1MB
    if request.content_length > 1024 * 1024:
        print('Request data size too big.')
        flash('Request data size too big.')
        abort(400)
    payload = request.get_data()
    sig_header = request.environ.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = endpoint_secret
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret)
    except ValueError as e:
        # Invalid payload
        flash('Invalid payload')
        return jsonify ({ }), 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        flash('Invalid signature')
        return jsonify ({ }), 400

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print(session)
        line_items = stripe.checkout.Session.list_line_items(session['id'], limit=1)
        print(line_items['data'][0]['description'])

    return jsonify ({ })

