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

def set_storage_quantity():
    from cart import get_items

    items = get_items()
    products = get_products()
    for item in items:
        for product in products:
            if item['id'] == product['id']:
                product['storage_quantity'] -= item['quantity']
            if product['storage_quantity'] < 0:
                product['storage_quantity'] = 0
    save_products(products)

def add_order_id(orders):
    order_id = 0
    for order in orders:
        order_id += 1
        order['id'] = order_id

def create_order_from_cart(orders, user_form_data, order, order_status, date_unix, date_time):
    orders.append(user_form_data | order | order_status | date_unix | date_time)
    # orders.append(request.form | cart.get_order() | {'status': "To do"} | {'date_unix': int(get_time_unix())} | {'date_time': str(get_date_time())})    