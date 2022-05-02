from flask import session
from . import data_manipulations


def new_order():
    session['current_order'] = {'items': []}
    session.modified = True


def add_item(item_id):
    items = session['current_order']['items']
    for cart_item in items:
        if cart_item['id'] == item_id:
            cart_item['quantity'] += 1
    else:
        products = data_manipulations.get_products()
        item = next(i for i in products if i['id'] == item_id)
        item['quantity'] = 1
        session['current_order']['items'].append(item)
    session.modified = True


def has_order():
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


def get_order():
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
    order = get_order()
    for item in order['items']:
        sum += int(item['price'])*item['quantity']
    return sum


def clear():
    session.clear()
