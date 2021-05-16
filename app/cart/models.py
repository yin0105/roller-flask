from app import db


class Cart(db.Model):
	__tablename__ = 'cart'
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	cart_items = db.relationship('CartItem', 
		foreign_keys='CartItem.cart_id', backref='cart', lazy='dynamic')
	# 'owner' property defined in User.cart via backref.

	def __repr__(self):
		return '<Cart {}>'.format(self.user_id)

	def get_currency(self):
		for cart_item in self.cart_items:
			if any(cart_item.currency for cart_item in self.cart_items):
				currency = cart_item.currency
				return currency

	def count_total_items(self):
		total_items = 0
		for cart_item in self.cart_items:
			total_items = sum(cart_item.quantity for cart_item in self.cart_items)
		return total_items

	def count_total_amount(self):
		total_amount = 0
		for cart_item in self.cart_items:
			total_amount = sum(cart_item.ttl_amount for cart_item in self.cart_items)
			return total_amount


class CartItem(db.Model):
	__tablename__ = 'cart_item'
	id = db.Column(db.Integer, primary_key=True)
	product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
	product = db.relationship('Product', backref=db.backref('cart_item', uselist=False))
	supplier_id = db.Column(db.Integer, db.ForeignKey('company.id'))
	brand = db.Column(db.String(64), index=True)
	model = db.Column(db.String(128), index=True)
	currency = db.Column(db.String(128))
	amount = db.Column(db.Integer())
	discount = db.Column(db.Integer())
	quantity = db.Column(db.Integer)
	ttl_amount = db.Column(db.Integer())
	feature_picture = db.Column(db.String(64), nullable=True, default='default.jpeg')
	cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'))
	order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
	incoming_order_id = db.Column(db.Integer, db.ForeignKey('incoming_order.id'))
	# 'cart' property defined in Cart.cart_items via backref.
	# 'order' property defined in Order.cart_items via backref.
	# 'supplier' property defined in Company.cart_items via backref.

	def __repr__(self):
		return '<CartItem {}>'.format(self.product_id)
