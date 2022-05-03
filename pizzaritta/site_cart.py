from flask import Blueprint, render_template, redirect, url_for, request
from . import data_manipulations
from . import notifications
from . import cart_manipulations

site_cart = Blueprint('site_cart', __name__, template_folder='templates')


@site_cart.route('/item/add_to_cart/<int:item_id>')
def add_to_cart(item_id):
    item = data_manipulations.get_product(item_id)
    if not cart_manipulations.has_order():
        cart_manipulations.new_order()
    cart_manipulations.add_item(item_id)
    notifications.add_notification(f"{item['name']} was added to cart")
    return redirect(url_for('site_catalog.index'))


@site_cart.route('/cart/delete_from_cart/<int:item_id>')
def delete_from_cart(item_id):
    cart_manipulations.delete_item(item_id)
    item = data_manipulations.get_product(item_id)
    notifications.add_notification(f"{item['name']} was removed")
    return redirect(url_for('site_cart.cart_list'))


@site_cart.route('/cart/remove_one_item/<int:item_id>')
def remove_one_item(item_id):
    cart_item = cart_manipulations.get_cart_item(item_id)
    if cart_item['quantity'] > 1:
        cart_manipulations.set_quantity(item_id, cart_item['quantity'] - 1)
        print(cart_item['quantity'])
    if cart_item['quantity'] == 1:
        cart_manipulations.delete_item(item_id)
    notifications.add_notification(f"{cart_item['name']} was removed")
    return redirect(url_for('site_cart.cart_list'))


@site_cart.route('/cart/add_one_item/<int:item_id>')
def add_one_pizza(item_id):
    cart_item = cart_manipulations.get_cart_item(item_id)
    cart_manipulations.set_quantity(item_id, cart_item['quantity'] + 1)
    notifications.add_notification(f"{cart_item['name']} was added to cart")
    return redirect(url_for('site_cart.cart_list'))


@site_cart.route('/cart')
def cart_list():
    if cart_manipulations.has_order():
        return render_template('cart.html', order=cart_manipulations.get_order(), notifications=notifications.get_notifications(), sum=cart_manipulations.get_order_sum())
    return render_template('cart.html', order=[], notifications=notifications.get_notifications())


@site_cart.route('/ordering')
def ordering():
    if cart_manipulations.has_order():
        return render_template('ordering.html', order=cart_manipulations.get_order(), notifications=notifications.get_notifications(), sum=cart_manipulations.get_order_sum())
    return render_template('ordering.html', order=[], notifications=notifications.get_notifications())


@site_cart.route('/create_order', methods=['POST'])
def create_order():
    data_manipulations.create_order_from_cart(request.form, cart_manipulations.get_order())
    cart_manipulations.clear()
    return redirect("/")

