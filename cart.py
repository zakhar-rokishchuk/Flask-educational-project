from flask import session
from data_manipulations import get_products


def new_order(item_id):
    session['current_order'] = {'items': []}
    session.modified = True

def add_item(item_id):
    products = get_products()
    item = next(i for i in products if i['id'] == item_id)
    item['quantity'] = 1
    session['current_order']['items'].append(item)

def has_order():
    if 'current_order' in session:
        return True
    else:
        return False

def get_items():
    return session['current_order']['items']

def get_order():
    return session['current_order']

