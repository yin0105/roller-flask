from flask import render_template, redirect, url_for, session
from flask_login import current_user, login_required

from app import db
from app.order import order_blueprint
from app.order.models import Order, IncomingOrder
from app.cart.models import Cart, CartItem
from app.user.models import User
from app.company.models import Company
from app.product.models import Product


@order_blueprint.route('/dashboard/<int:user_id>', methods=['GET', 'POST'])
@login_required
def dashboard(user_id):
	user = User.query.get_or_404(current_user.id)
	orders = Order.query.join(Order.buyer).filter(User.id==user_id)
	session['ORDER'] = orders.count()
	return render_template('order/dashboard.html', title='Order', 
													user=user, 
													orders=orders)


@order_blueprint.route('/order_id/<int:order_id>/<int:company_id>', methods=['GET', 'POST'])
@login_required
def show(order_id, company_id):
	order = Order.query.get_or_404(order_id)
	company = Company.query.get_or_404(company_id)
	user_id = order.buyer_id
	cart = Cart.query.join(Order.buyer).filter(User.id==user_id)
	currency = order.get_currency()

	if any(cart_item.product.company_id==company.id for cart_item in order.cart_items):
		cart_items = CartItem.query.filter(CartItem.order_id==order.id).join(CartItem.product).\
									filter(Product.supplier==company).all()
		print(f'{cart_items}')

	def count_supplier_total_items():
		supplier_total_items=0 
		for cart_item in cart_items:
			supplier_total_items = sum(cart_item.quantity for cart_item in cart_items)
			return supplier_total_items
	supplier_total_items = count_supplier_total_items()

	def count_supplier_total_amount():
		supplier_total_amount=0 
		for cart_item in cart_items:
			supplier_total_amount = sum(cart_item.ttl_amount for cart_item in cart_items)
			return supplier_total_amount
	supplier_total_amount = count_supplier_total_amount()

	return render_template('order/show.html', title='Order', 
												order=order, 
												company=company,  
												cart=cart, 
												user_id=user_id, 
												currency=currency, 
												cart_items=cart_items,  
												supplier_total_items=supplier_total_items, 
												supplier_total_amount=supplier_total_amount)


@order_blueprint.route('/incoming_order_id/<int:incoming_order_id>/company_id/<int:company_id>', methods=['GET', 'POST'])
@login_required
def incoming(incoming_order_id, company_id):
	incoming_order = IncomingOrder.query.get_or_404(incoming_order_id)
	company = Company.query.get_or_404(company_id)
	supplier_total_items = incoming_order.count_supplier_total_items()
	supplier_total_amount = incoming_order.count_supplier_total_amount()
	return render_template('order/incoming_order.html', title='Order', 
														incoming_order=incoming_order, 
														company=company,  
														supplier_total_items=supplier_total_items, 
														supplier_total_amount=supplier_total_amount)


@order_blueprint.route('/delete/incoming_order_id/<int:incoming_order_id>/company_id/<int:company_id>', methods=['GET', 'POST'])
@login_required
def remove_incoming_item(incoming_order_id, company_id):
	incoming_order = IncomingOrder.query.get_or_404(incoming_order_id)
	company = Company.query.get_or_404(company_id)
	#company.incoming_orders.remove(incoming_order)
	db.session.delete(incoming_order)
	db.session.commit()
	return redirect(url_for('company.shop', company_id=company.id))
