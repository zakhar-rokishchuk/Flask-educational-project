from itertools import product
from flask import Flask, render_template, url_for, session, redirect
from products import PRODUCTS
from orders import ORDERS


app = Flask(__name__)


app.secret_key = b'SAJGDD&S^ATDIGU^%)_'


@app.route('/')
def index():
    return render_template('index.html', items=PRODUCTS, notifications=get_notifications())


@app.route('/item/<int:item_id>')
def item(item_id):
    item = next(i for i in PRODUCTS if i['id'] == item_id)
    return render_template('item.html', item=item)


def add_item(item_id):
    item = next(i for i in PRODUCTS if i['id'] == item_id)
    item['quantity'] = 1
    session['current_order']['items'].append(item)


def remove_item(item_id):
    item = next(i for i in PRODUCTS if i['id'] == item_id)
    item['quantity'] = 1
    session['current_order']['items'].remove(item)


def init_cart_cookies(item_id):
    session['current_order'] = {'items': [], 'payment_method': 'cash'}


def add_notification(message):
    if not 'notifications' in session:
        session['notifications'] = []
    notification = {'message': message}
    # add notification creation date, time (timestamp)
    session['notifications'].append(notification)


def get_notifications():
    if not 'notifications' in session:
        session['notifications'] = []
    # filter notifications by date and show notifications for last minute
    return session['notifications']


@app.route('/item/add_to_cart/<int:item_id>')
def add_to_cart(item_id):
    if not 'current_order' in session:
        init_cart_cookies(item_id)
    session.modified = True
    cart_list = session['current_order']['items']
    is_pizza_in_order = False
    for cart_item in cart_list:
        if item_id == cart_item['id']:
            is_pizza_in_order = True
            cart_item['quantity'] += 1
    if is_pizza_in_order == True:
        pass
    else:
        add_item(item_id)
        added_pizza = next(i for i in cart_list if i['id'] == item_id)
        add_notification(f"{added_pizza['name']} WAS ADDED TO CART!")
    return redirect(url_for('index'))


@app.route('/cart/delete_from_cart/<int:item_id>')
def delete_from_cart(item_id):
    cart_list = session['current_order']['items']
    for cart_item in cart_list:
        session.modified = True
        if item_id == cart_item['id']:
            cart_list.remove(cart_item)
    return redirect(url_for('cart'))


@app.route('/cart/remove_one_pizza/<int:item_id>')
def remove_one_pizza(item_id):
    cart_list = session['current_order']['items']
    for cart_item in cart_list:
        quantity = cart_item['quantity']
        session.modified = True
        if item_id == cart_item['id']:
            if quantity > 1:
                quantity -= 1
            elif quantity == 1:
                cart_list.remove(cart_item)
    return redirect(url_for('cart'))


@app.route('/cart/add_one_pizza/<int:item_id>')
def add_one_pizza(item_id):
    cart_list = session['current_order']['items']
    for cart_item in cart_list:
        session.modified = True
        if item_id == cart_item['id']:
            cart_item['quantity'] += 1
    return redirect(url_for('cart'))


@app.route('/cart/change_payment_method/<payment_method>')
def change_payment_method(payment_method):
    session.modified = True
    if 'current_order' in session:
        session['current_order']['payment_method'] = payment_method
    else:
        init_cart_cookies()
        session['current_order']['payment_method'] = payment_method
    return redirect(url_for('cart'))


@app.route('/cart_check')
def cart_check():
    return session['current_order']


@app.route('/cart')
def cart():
    if 'current_order' in session:
        return render_template('cart.html', order=session['current_order'])
    else:
        return render_template('cart.html', order=[])


@app.route('/admin')
def admin():
    return render_template('admin_base.html')


@app.route('/admin/products')
def admin_products():
    return render_template('products.html', items=PRODUCTS)


@app.route('/admin/orders')
def admin_clients():
    return render_template('orders.html', orders=ORDERS)


if __name__ == "__main__":
    app.run(debug=True)
