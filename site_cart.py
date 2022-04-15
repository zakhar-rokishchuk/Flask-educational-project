from flask import Blueprint, render_template, redirect, url_for, request
from data_manipulations import add_order_id, create_order_from_cart, get_product, get_orders, set_storage_quantity, save_orders
from notifications import get_notifications, add_notification
from time_record import get_date_time, get_time_unix
import cart

site_cart = Blueprint('site_cart', __name__, template_folder='templates')


@site_cart.route('/item/add_to_cart/<int:item_id>')
def add_to_cart(item_id):
    item = get_product(item_id)
    if not cart.has_order():
        cart.new_order()
    cart.add_item(item_id)
    add_notification(f"{item['name']} WAS ADDED TO CART")
    return redirect(url_for('site_catalog.index'))


@site_cart.route('/cart/delete_from_cart/<int:item_id>')
def delete_from_cart(item_id):
    cart.delete_item(item_id)
    item = get_product(item_id)
    add_notification(f"{item['name']} WAS REMOVED")
    return redirect(url_for('site_cart.cart_list'))


@site_cart.route('/cart/remove_one_item/<int:item_id>')
def remove_one_item(item_id):
    cart_item = cart.get_cart_item(item_id)
    if cart_item['quantity'] > 1:
        cart.set_quantity(item_id, cart_item['quantity'] - 1)
    if cart_item['quantity'] == 1:
        cart.delete_item(item_id)
    add_notification(f"{cart_item['name']} WAS REMOVED")
    return redirect(url_for('site_cart.cart_list'))


@site_cart.route('/cart/add_one_item/<int:item_id>')
def add_one_pizza(item_id):
    cart_item = cart.get_cart_item(item_id)
    cart.set_quantity(item_id, cart_item['quantity'] + 1)
    add_notification(f"{cart_item['name']} WAS ADDED TO CART!")
    return redirect(url_for('site_cart.cart_list'))


@site_cart.route('/cart')
def cart_list():
    if cart.has_order():
        return render_template('cart.html', order=cart.get_order(), notifications=get_notifications(), sum=cart.get_order_sum())
    return render_template('cart.html', order=[], notifications=get_notifications())


@site_cart.route('/ordering')
def ordering():
    if cart.has_order():
        return render_template('ordering.html', order=cart.get_order(), notifications=get_notifications(), sum=cart.get_order_sum())
    else:
        return render_template('ordering.html', order=[], notifications=get_notifications())


@site_cart.route('/create_order', methods=['POST'])
def create_order():
    orders = get_orders()
    if request.method == "POST":
        create_order_from_cart(orders, request.form, cart.get_order(), {'status': "To do"}, {
                               'date_unix': int(get_time_unix())}, {'date_time': str(get_date_time())})
        set_storage_quantity()
        add_order_id(orders)
        save_orders(orders)
        cart.clear()
        return redirect("/")
    return render_template('ordering.html', order=cart.get_order())
