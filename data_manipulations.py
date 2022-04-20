from flask import request
import json
from time_record import get_date_time, get_time_unix


def get_products():
    with open("products.json", "r") as file:
        products = json.loads(file.read())
    return products


def get_orders():
    with open("orders.json", "r") as file:
        orders = json.loads(file.read())
    return orders


def save_products(products):
    json_products_list = json.dumps(products)
    with open("products.json", "w") as file:
        file.write(json_products_list)


def save_orders(orders):
    json_full_order = json.dumps(orders)
    with open("orders.json", "w") as file:
        file.write(json_full_order)


def get_product(product_id):
    products = get_products()
    product = next(i for i in products if i['id'] == product_id)
    return product


def get_order(order_id):
    orders = get_orders()
    order = next(i for i in orders if i['id'] == order_id)
    return order


def get_products_to_display():
    products = get_products()
    products_to_display = []
    for product in products:
        if product["display"] == "On":
            products_to_display.append(product)
    return products_to_display


def update_storage_quantity_with_order(order):
    products = get_products()
    for item in order['items']:
        for product in products:
            if item['id'] == product['id']:
                product['storage_quantity'] -= item['quantity']
            if product['storage_quantity'] < 0:
                product['storage_quantity'] = 0
    save_products(products)


def get_new_order_id(orders):
    orders = get_orders()
    if not orders[-1]['id']:
        new_order_id = 1
    new_order_id = orders[-1]['id'] + 1
    return new_order_id


def create_order_from_cart2(orders, user_form_data, order, order_status, date_unix, date_time):
    orders.append(user_form_data | order |
                  order_status | date_unix | date_time)


def create_order_from_cart(user_form_data, order):
    order_data = user_form_data | order | {'status': "To do"} | {
        'date_unix': int(get_time_unix())} | {'date_time': str(get_date_time())}
    create_order(order_data)


def create_order(order):
    orders = get_orders()
    id = get_new_order_id(orders)
    orders.append(order | {'id': id})
    update_storage_quantity_with_order(order)
    save_orders(orders)


def filter_orders_by_status():
    filtered_orders = []
    orders = get_orders()
    for order in orders:
        if order["status"] == request.args.get("filter_orders"):
            filtered_orders.append(order)
    return filtered_orders


def sort_orders_by_date():
    orders = get_orders()
    return sorted(orders, key=lambda order: order['date_unix'], reverse=True)


def filter_orders_by_name():
    filtered_orders = []
    orders = get_orders()
    for order in orders:
        if request.args.get("search_name").lower() in order["name"].lower():
            filtered_orders.append(order)
    return filtered_orders


