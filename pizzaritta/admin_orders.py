from flask import Blueprint, render_template, redirect, request
from . import db_orders_manipulations


admin_orders = Blueprint('admin_orders', __name__,
                         template_folder='templates')


@admin_orders.route('/admin')
@admin_orders.route('/admin/orders')
def orders():
    if request.args.get("filter_orders"):
        return render_template('orders.html', orders=db_orders_manipulations.filter_orders_by_status(request.args.get("filter_orders")))
    if request.args.get("search_name"):
        return render_template('orders.html', orders=db_orders_manipulations.filter_orders_by_name(request.args.get("search_name")))
    return render_template('orders.html', orders=db_orders_manipulations.get_orders())


@admin_orders.route('/admin/orders/<int:order_id>', methods=["GET"])
def order(order_id):
    order, order_items = db_orders_manipulations.get_order(order_id)
    return render_template('order.html', order=order, order_items=order_items)


@admin_orders.route('/admin/orders/<int:order_id>/comments', methods=["POST"])
def order_post_comment(order_id):
    db_orders_manipulations.add_comments(order_id, request.form["comment"])
    return render_template('order.html', order=db_orders_manipulations.get_order(order_id))


@admin_orders.route('/admin/orders/<int:order_id>/edit', methods=["GET"])
def editing_order(order_id):
    order, order_items = db_orders_manipulations.get_order(order_id)
    return render_template('editing_order.html', order=order, order_items=order_items)


@admin_orders.route('/admin/orders/<int:order_id>/edit', methods=["POST"])
def save_edited_order(order_id):
    _order, order_items = db_orders_manipulations.get_order(order_id)
    products_to_update = []
    for product in order_items:
        if request.form[f"item_{product['id']}_quantity"] != product['quantity']:
            products_to_update.append(product)
    db_orders_manipulations.update_order(order_id, 
                                         request.form["date_time"], 
                                         request.form["user_name"], 
                                         request.form["address"], 
                                         request.form["phone"], 
                                         request.form["payment_method"], 
                                         request.form["status"]) 
    for product in products_to_update:
        db_orders_manipulations.update_order_product_quantity(order_id, product['id'], request.form[f"item_{product['id']}_quantity"])
    return redirect("/admin/orders")


@admin_orders.route('/admin/orders/<int:order_id>/status', methods=['POST'])
def change_status(order_id):
    db_orders_manipulations.change_status(order_id, request.form["order_status_form"])
    return redirect("/admin/orders")
