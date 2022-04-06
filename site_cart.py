from flask import Blueprint, render_template, abort, redirect, url_for, session, request
from data_manipulations import get_products, save_products, get_product, get_products_to_display, get_orders, save_orders, get_order
from notifications import get_notifications, add_notification
import json
from time_record import get_date_time, get_time_unix
import cart

site_cart = Blueprint('site_cart', __name__,
                        template_folder='templates')


@site_cart.route('/item/add_to_cart/<int:item_id>')
def add_to_cart(item_id):
    added_pizza = init_added_pizza(item_id)
    if not cart.has_order():
        cart.new_order(item_id)
    cart_list = cart.get_items()
    is_pizza_in_order = False
    for cart_item in cart_list:
        if item_id == cart_item['id']:
            is_pizza_in_order = True
            cart_item['quantity'] += 1
            add_notification(f"{added_pizza['name']} WAS ADDED TO CART")
    if is_pizza_in_order == True:
        pass
    else:
        cart.add_item(item_id)
        add_notification(f"{added_pizza['name']} WAS ADDED TO CART")
    return redirect(url_for('site_catalog.index'))

def init_added_pizza(item_id):
    products = get_products()
    return next(i for i in products if i['id'] == item_id)

@site_cart.route('/cart/delete_from_cart/<int:item_id>')
def delete_from_cart(item_id):
    added_pizza = init_added_pizza(item_id)
    cart_list = cart.get_items()
    for cart_item in cart_list:
        session.modified = True
        if item_id == cart_item['id']:
            add_notification(f"{added_pizza['name']} WAS REMOVED")
            cart_list.remove(cart_item)
    return redirect(url_for('cart'))

@site_cart.route('/cart/remove_one_pizza/<int:item_id>')
def remove_one_pizza(item_id):
    added_pizza = init_added_pizza(item_id)
    cart_list = cart.get_items()
    for cart_item in cart_list:
        session.modified = True
        if item_id == cart_item['id']:
            if cart_item['quantity'] > 1:
                cart_item['quantity'] -= 1
                add_notification(f"{added_pizza['name']} WAS REMOVED")
            elif cart_item['quantity'] == 1:
                add_notification(f"{added_pizza['name']} WAS REMOVED")
                cart_list.remove(cart_item)
    return redirect(url_for('site_cart.cart'))

@site_cart.route('/cart/add_one_pizza/<int:item_id>')
def add_one_pizza(item_id):
    added_pizza = init_added_pizza(item_id)
    cart_list = cart.get_items()
    for cart_item in cart_list:
        session.modified = True
        if item_id == cart_item['id']:
            # FIXME 
            cart_item['quantity'] += 1
            add_notification(f"{added_pizza['name']} WAS ADDED TO CART!")
    return redirect(url_for('site_cart.cart'))

@site_cart.route('/cart')
def cart():
    if cart.has_order():
        return render_template('cart.html', order=cart.get_order(), notifications=get_notifications(), sum=order_sum())
    else:
        return render_template('cart.html', order=[], notifications=get_notifications())

@site_cart.route('/ordering')
def ordering():
    if cart.has_order():
        return render_template('ordering.html', order=cart.get_order(), notifications=get_notifications(), sum=order_sum())
    else:
        return render_template('ordering.html', order=[], notifications=get_notifications())

@site_cart.route('/create_order', methods=['POST'])
def create_order():
    if request.method == "POST":
        session.modified = True
        orders = get_orders()
        products = get_products()
        orders.append(
            request.form | cart.get_order() |
            {'status': "To do"} | {'date_unix': int(get_time_unix())} | {'date_time': str(get_date_time())})
        for item in session['current_order']['items']:
            for product in products:
                if item['id'] == product['id']:
                    product['storage_quantity'] -= item['quantity']
                if product['storage_quantity'] < 0:
                    product['storage_quantity'] = 0
        order_id = 0
        for order in orders:
            order_id += 1
            order['id'] = order_id
        save_orders(orders)
        save_products(products)
        session.clear()
        return redirect("/")
    return render_template('ordering.html', order=cart.get_order())

def order_sum():
    sum = 0
    order = cart.get_order()
    for item in order['items']:
        sum += int(item['price'])*item['quantity']
    return sum
