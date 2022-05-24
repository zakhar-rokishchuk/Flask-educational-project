import imp
from itertools import product
import json
import psycopg2
import psycopg2.extras


def get_products():
    conn = psycopg2.connect("dbname=pizzaritta user=zakharrokishchuk")
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cur.execute("select * from products;")
    products = cur.fetchall()
    return products
    # print(products)
    # print(products['name'])
    # cur.close()
    # conn.close()
    # with open("products.json", "r") as file:
    #     products = json.loads(file.read())
    # return products


def get_products_to_display():
    products = get_products()
    products_to_display = []
    for product in products:
        if product["display"] == "On":
            products_to_display.append(product)
    return products_to_display