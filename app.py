from itertools import product
from flask import Flask, render_template, url_for, session
from products import PRODUCTS
from orders import ORDERS


app = Flask(__name__)


app.secret_key = b'SAJGDD&S^ATDIGU^%)_'


@app.route('/')
def index():
    return render_template('index.html', items=PRODUCTS)


@app.route('/item/<int:item_id>')
def item(item_id):
    item = next(i for i in PRODUCTS if i['id'] == item_id)
    return render_template('item.html', item=item)


@app.route('/item/add_to_cart/<int:item_id>')
def add_to_cart(item_id):
    if not 'current_order' in session:
        session['current_order'] = {
            'items': [],
            'payment_method': 'cash'
        }
    item = next(i for i in PRODUCTS if i['id'] == item_id)
    item['quantity'] = 1
    session['current_order']['items'].append(item)
    return session['current_order']


@app.route('/cart')
def cart():
    return render_template('cart.html', order=session['current_order'])


@app.route('/admin')
def admin():
    return render_template('admin_base.html')


@app.route('/admin/products')
def admin_products():
    return render_template('products.html', items=PRODUCTS)


@app.route('/admin/orders')
def admin_clients():
    return render_template('orders.html', orders=ORDERS)


if __name__ == "__main__":
    app.run(debug=True)
