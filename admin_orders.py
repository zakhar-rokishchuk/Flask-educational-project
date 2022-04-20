from flask import Blueprint, render_template, redirect, session, request
from data_manipulations import filter_orders_by_name, filter_orders_by_status, get_orders, save_orders, get_order, sort_orders_by_date
import json

admin_orders = Blueprint('admin_orders', __name__,
                         template_folder='templates')


@admin_orders.route('/admin')
@admin_orders.route('/admin/orders')
def orders():
    # filtered_orders = []
    # orders = get_orders()
    if request.args.get("filter_orders"):
        # for order in orders:
        #     if order["status"] == request.args.get("filter_orders"):
        #         filtered_orders.append(order)
        return render_template('orders.html', orders=filter_orders_by_status())

    # sorted_full_order = sorted(
    #     orders, key=lambda order: order['date_unix'], reverse=True)
    if request.args.get("search_name"):
        # for order in orders:
        #     if request.args.get("search_name").lower() in order["name"].lower():
        #         filtered_orders.append(order)
        return render_template('orders.html', orders=filter_orders_by_name())
    return render_template('orders.html', orders=sort_orders_by_date())


@admin_orders.route('/admin/orders/<int:order_id>', methods=["GET", "POST"])
def order(order_id):
    orders = get_orders()
    order = next(i for i in orders if i['id'] == order_id)
    if request.method == "POST":
        order["comment"] = request.form["comment"]
    save_orders(orders)
    return render_template('order.html', order=order)


@admin_orders.route('/admin/orders/<int:order_id>/edit', methods=["GET", "POST"])
def edit_order(order_id):
    orders = get_orders()
    order = next(i for i in orders if i['id'] == order_id)
    return render_template('editing_order.html', order=order)


@admin_orders.route('/admin/orders/<int:order_id>/edit/save', methods=["POST"])
def save_order(order_id):
    orders = get_orders()
    if request.method == "POST":

        session.modified = True

        order = next(
            order for order in orders if order['id'] == order_id)
        order['name'] = request.form["name"]
        order['address'] = request.form["address"]
        order['phone'] = request.form["phone"]
        order['payment_method'] = request.form["payment_method"]
        order["status"] = request.form["status"]
        for item in order['items']:
            input_name = "item_"+str(item['id'])+"_quantity"
            item['quantity'] = request.form[input_name]
        save_orders(orders)
    return redirect("/admin/orders")


@admin_orders.route('/admin/orders/<int:order_id>/status', methods=['POST'])
def change_status(order_id):
    if request.method == "POST":
        session.modified = True
        with open("orders.json", "r") as file:
            full_order = json.loads(file.read())
        order_to_change = next(
            order for order in full_order if order['id'] == order_id)
        order_to_change['status'] = request.form["order_status_form"]
        json_full_order = json.dumps(full_order)
        with open("orders.json", "w") as file:
            file.write(json_full_order)
    return redirect("/admin/orders")
