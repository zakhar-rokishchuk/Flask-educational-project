from webbrowser import get
from flask import Blueprint, render_template, redirect, session, request
from . import data_manipulations
import json

admin_orders = Blueprint('admin_orders', __name__,
                         template_folder='templates')


@admin_orders.route('/admin')
@admin_orders.route('/admin/orders')
def orders():
    if request.args.get("filter_orders"):
        return render_template('orders.html', orders=data_manipulations.filter_orders_by_status(request.args.get("filter_orders")))
    if request.args.get("search_name"):
        return render_template('orders.html', orders=data_manipulations.filter_orders_by_name(request.args.get("search_name")))
    return render_template('orders.html', orders=data_manipulations.sort_orders_by_date())


@admin_orders.route('/admin/orders/<int:order_id>', methods=["GET"])
def order(order_id):
    return render_template('order.html', order=data_manipulations.get_order(order_id))


@admin_orders.route('/admin/orders/<int:order_id>/comments', methods=["POST"])
def order_post_comment(order_id):
    order = data_manipulations.get_order(order_id)
    order['comment'] = request.form["comment"]
    data_manipulations.save_order(order)
    return render_template('order.html', order=data_manipulations.get_order(order_id))


@admin_orders.route('/admin/orders/<int:order_id>/edit', methods=["GET"])
def edit_order(order_id):
    return render_template('editing_order.html', order=data_manipulations.get_order(order_id))


@admin_orders.route('/admin/orders/<int:order_id>/edit', methods=["POST"])
def save_edited_order(order_id):
    order = data_manipulations.get_order(order_id)
    order['name'] = request.form["name"]
    order['address'] = request.form["address"]
    order['phone'] = request.form["phone"]
    order['payment_method'] = request.form["payment_method"]
    order["status"] = request.form["status"]
    for item in order['items']:
        input_name = "item_"+str(item['id'])+"_quantity"
        item['quantity'] = request.form[input_name]
    data_manipulations.save_order(order)
    return redirect("/admin/orders")


@admin_orders.route('/admin/orders/<int:order_id>/status', methods=['POST'])
def change_status(order_id):
    order = data_manipulations.get_order(order_id)
    order['status'] = request.form["order_status_form"]
    data_manipulations.save_order(order)
    return redirect("/admin/orders")
