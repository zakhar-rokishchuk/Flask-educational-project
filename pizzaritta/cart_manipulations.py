from flask import session
from pizzaritta import db_orders_manipulations
from . import db_products_manipulations
import psycopg2
from . import time_record


def connect_to_db():
    conn = psycopg2.connect("dbname=pizzaritta user=zakharrokishchuk")
    return conn


def disconnect_from_db(conn, cur):
    cur.close()
    conn.close()


def new_order():
    session['current_order'] = {'items': []}
    session.modified = True


def add_item(item_id):
    items = session['current_order']['items']
    for cart_item in items:
        if cart_item['id'] == item_id:
            cart_item['quantity'] += 1
    products = db_products_manipulations.get_products()
    item = next(i for i in products if i['id'] == item_id)
    item['quantity'] = 1
    session['current_order']['items'].append(item)
    session.modified = True


def has_current_order():
    if 'current_order' in session:
        return True
    else:
        return False


def get_items():
    return session['current_order']['items']


def get_cart_item(item_id):
    items = session['current_order']['items']
    item = next(i for i in items if i['id'] == item_id)
    return item


def get_current_order():
    return session['current_order']


def delete_item(item_id):
    items = get_items()
    for cart_item in items:
        session.modified = True
        if item_id == cart_item['id']:
            items.remove(cart_item)


def set_quantity(item_id, quantity):
    items = session['current_order']['items']
    item = next(i for i in items if i['id'] == item_id)
    item['quantity'] = quantity
    session.modified = True


def get_order_sum():
    sum = 0
    order = get_current_order()
    for item in order['items']:
        sum += int(item['price'])*item['quantity']
    return sum


def clear_session():
    session.clear()


def create_order_from_cart(user_data, order):
    conn = connect_to_db()
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cur.execute(f"""insert into orders (date_time, user_name, address, phone, payment_method, status) 
                                values ('{time_record.get_date_time()}', 
                                        '{user_data['name']}', 
                                        '{user_data['address']}',
                                        '{user_data['phone']}',
                                        '{user_data['payment_method']}',
                                        'To do');""")
    conn.commit()
    cur.execute("select max(id) as id from orders;")
    order_id = cur.fetchone()
    for product in order['items']:
        cur.execute(f"""insert into order_products (order_id, product_id, quantity) 
                                    values ({order_id['id']},
                                            {product['id']},
                                            {product['quantity']});""")
    conn.commit()                 
    disconnect_from_db(conn, cur)


