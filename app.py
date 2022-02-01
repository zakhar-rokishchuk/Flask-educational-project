from itertools import product
from traceback import print_tb
from flask import Flask, render_template, request, url_for, session, redirect
from products import PRODUCTS
from datetime import datetime
import time
import json

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


def init_added_pizza(item_id):
    return next(i for i in PRODUCTS if i['id'] == item_id)


def get_time_unix():
    return time.mktime(datetime.now().timetuple())


def add_notification(message):
    if not 'notifications' in session:
        session['notifications'] = []
    notification = {'message': message, 'time': get_time_unix()}
    session['notifications'].append(notification)


def get_notifications():
    if not 'notifications' in session:
        session['notifications'] = []
    for notification in session['notifications']:
        session.modified = True
        current_time = get_time_unix()
        if int((current_time - 2)) > int(notification['time']):
            session['notifications'].remove(notification)
    # filter notifications by date and show notifications for last minute
    return session['notifications']


@app.route('/item/add_to_cart/<int:item_id>')
def add_to_cart(item_id):
    added_pizza = init_added_pizza(item_id)
    if not 'current_order' in session:
        init_cart_cookies(item_id)
    session.modified = True
    cart_list = session['current_order']['items']
    is_pizza_in_order = False
    for cart_item in cart_list:
        if item_id == cart_item['id']:
            is_pizza_in_order = True
            cart_item['quantity'] += 1
            add_notification(f"{added_pizza['name']} WAS ADDED TO CART")
    if is_pizza_in_order == True:
        pass
    else:
        add_item(item_id)
        add_notification(f"{added_pizza['name']} WAS ADDED TO CART")
    return redirect(url_for('index'))


@app.route('/cart/delete_from_cart/<int:item_id>')
def delete_from_cart(item_id):
    added_pizza = init_added_pizza(item_id)
    cart_list = session['current_order']['items']
    for cart_item in cart_list:
        session.modified = True
        if item_id == cart_item['id']:
            add_notification(f"{added_pizza['name']} WAS REMOVED")
            cart_list.remove(cart_item)
    return redirect(url_for('cart'))


@app.route('/cart/remove_one_pizza/<int:item_id>')
def remove_one_pizza(item_id):
    added_pizza = init_added_pizza(item_id)
    cart_list = session['current_order']['items']
    for cart_item in cart_list:
        session.modified = True
        if item_id == cart_item['id']:
            if cart_item['quantity'] > 1:
                cart_item['quantity'] -= 1
                add_notification(f"{added_pizza['name']} WAS REMOVED")
            elif cart_item['quantity'] == 1:
                add_notification(f"{added_pizza['name']} WAS REMOVED")
                cart_list.remove(cart_item)
    return redirect(url_for('cart'))


@app.route('/cart/add_one_pizza/<int:item_id>')
def add_one_pizza(item_id):
    added_pizza = init_added_pizza(item_id)
    cart_list = session['current_order']['items']
    for cart_item in cart_list:
        session.modified = True
        if item_id == cart_item['id']:
            cart_item['quantity'] += 1
            add_notification(f"{added_pizza['name']} WAS ADDED TO CART!")
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


def order_sum():
    sum = 0
    for item in session['current_order']['items']:
        session.modified = True
        sum += item['price']*item['quantity']
    return sum


@app.route('/cart_check')
def cart_check():
    return session['current_order']


@app.route('/cart')
def cart():
    if 'current_order' in session:
        return render_template('cart.html', order=session['current_order'], notifications=get_notifications(), sum=order_sum())
    else:
        return render_template('cart.html', order=[], notifications=get_notifications())


@app.route('/cart_order')
def cart_order():
    if 'current_order' in session:
        return render_template('cart_order.html', order=session['current_order'], notifications=get_notifications(), sum=order_sum())
    else:
        return render_template('cart_order.html', order=[], notifications=get_notifications())


@app.route('/create_order', methods=['POST'])
def create_order():
    if request.method == "POST":
        full_order = request.form | session['current_order']
        with open("orders.json", "w") as file:
            file.write(json.dumps(full_order))
    return render_template('cart_order.html', order=session['current_order'])


@app.route('/admin/orders')
def admin_clients():
    with open("orders.json", "r") as file: 
        json_full_order = json.load(file)
        print(type(json_full_order))

        for i in json_full_order:
            print(json_full_order[i])
    return render_template('orders.html', orders=json_full_order)


@app.route('/admin')
def admin():
    return render_template('admin_base.html')


@app.route('/admin/products')
def admin_products():
    return render_template('products.html', items=PRODUCTS)


if __name__ == "__main__":
    app.run(debug=True)
    app.run()
