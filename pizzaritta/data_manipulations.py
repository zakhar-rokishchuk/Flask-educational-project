from flask import request
import json
from . import time_record
from PIL import Image
import os
from . import config
from . import db_orders_manipulations


# def get_products():
#     with open("products.json", "r") as file:
#         products = json.loads(file.read())
#     return products


# def get_orders():
#     with open("orders.json", "r") as file:
#         orders = json.loads(file.read())
#     return orders


# def get_order(order_id):
#     orders = get_orders()
#     order = next(i for i in orders if i['id'] == order_id)
#     return order


# def save_products(products):
#     json_products_list = json.dumps(products)
#     with open("products.json", "w") as file:
#         file.write(json_products_list)


# def save_orders(orders):
#     json_full_order = json.dumps(orders)
#     with open("orders.json", "w") as file:
#         file.write(json_full_order)


# def save_order(order_to_save):
#     orders = get_orders()
#     order = next(i for i in orders if i['id'] == order_to_save['id'])
#     if 'comment' in order:
#         order['comment'] = order_to_save['comment']
#     order['name'] = order_to_save['name']
#     order['address'] = order_to_save['address']
#     order['phone'] = order_to_save['phone']
#     order['payment_method'] = order_to_save['payment_method']
#     order['status'] = order_to_save['status']
#     order['items'] = order_to_save['items']
#     save_orders(orders)


# def get_product(product_id):
#     products = get_products()
#     product = next(i for i in products if i['id'] == product_id)
#     return product


# def save_product(product_to_save):
#     products = get_products()
#     product = next(i for i in products if i['id'] == product_to_save['id'])
#     product['name'] = product_to_save['name']
#     product['price'] = product_to_save['price']
#     product['description'] = product_to_save['description']
#     product['short_description'] = product_to_save['short_description']
#     product['display'] = product_to_save['display']
#     product['img_src'] = product_to_save['img_src']
#     product['type'] = product_to_save['type']
#     product['quantity'] = product_to_save['quantity']
#     product['storage_quantity'] = product_to_save['storage_quantity']
#     save_products(products)


# def get_products_to_display():
#     products = get_products()
#     products_to_display = []
#     for product in products:
#         if product["display"] == "On":
#             products_to_display.append(product)
#     return products_to_display


# def update_storage_quantity_with_order(order):
#     products = get_products()
#     for item in order['items']:
#         for product in products:
#             if item['id'] == product['id']:
#                 product['storage_quantity'] -= item['quantity']
#             if product['storage_quantity'] < 0:
#                 product['storage_quantity'] = 0
#     save_products(products)


# def get_new_order_id(orders):
#     orders = get_orders()
#     if not orders[-1]['id']:
#         new_order_id = 1
#     new_order_id = orders[-1]['id'] + 1
#     return new_order_id


def create_order_from_cart2(orders, user_form_data, order, order_status, date_unix, date_time):
    orders.append(user_form_data | order |
                  order_status | date_unix | date_time)


# def filter_orders_by_status(status):
#     orders = get_orders()
#     filtered_orders = []
#     for order in orders:
#         if order["status"] == status:
#             filtered_orders.append(order)
#     return filtered_orders


# def sort_orders_by_date():
#     orders = get_orders()
#     return sorted(orders, key=lambda order: order['date_unix'], reverse=True)


# def filter_orders_by_name(name_to_search):
#     orders = get_orders()
#     filtered_orders = []
#     for order in orders:
#         if name_to_search.lower() in order["name"].lower():
#             filtered_orders.append(order)
#     return filtered_orders


# def add_comment_to_order(order_id):
#     orders = get_orders()
#     order = next(i for i in orders if i['id'] == order_id)
#     order["comment"] = request.form["comment"]
#     save_orders(orders)


# def filter_products_by_type(type):
#     products = get_products()
#     filtered_products = []
#     for product in products:
#             if product["type"] == type:
#                 filtered_products.append(product)
#     return filtered_products


# def resize_new_product_picture(filename, product_id):
#     image_path = Image.open(config.PATH_TO_IMAGES+filename)
#     new_image_163 = image_path.resize((163, 163))
#     new_image_333 = image_path.resize((333, 333)) 
#     new_image_555 = image_path.resize((555, 555))
#     new_image_163.save(config.PATH_TO_IMAGES+"163/163_"+product_id+".jpeg")
#     new_image_333.save(config.PATH_TO_IMAGES+"333/333_"+product_id+".jpeg")
#     new_image_555.save(config.PATH_TO_IMAGES+"555/555_"+product_id+".jpeg")
#     os.remove(config.PATH_TO_IMAGES+filename)