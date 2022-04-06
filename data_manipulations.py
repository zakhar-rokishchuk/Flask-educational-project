import json


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