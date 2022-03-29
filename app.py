from itertools import product
from traceback import print_tb
from flask import Flask, render_template, request, url_for, session, redirect, send_from_directory
from datetime import datetime
import time
import json
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = 'static/img'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = b'SAJGDD&S^ATDIGU^%)_'


@app.route('/')
def index():
    with open("products.json", "r") as file:
        PRODUCTS = json.loads(file.read())
    products_to_display = []
    for product in PRODUCTS:
        if product["display"] == "On":
            products_to_display.append(product)
    return render_template('index.html', items=products_to_display, notifications=get_notifications())


# @app.route('/test')
# def test():
    # size = (163, 163) 
    # image_path = Image.open("static/img/pesto.jpeg")
    # new_image = image_path.resize((163, 163))
    # new_image.save("static/img/pesto_163.jpeg")
    # directory = 'static/img/163'
    # for filename in os.listdir(directory):
    #     f = os.path.join(directory, filename)
    #     if os.path.isfile(f):
    #         image_path = Image.open(f)
    #         new_image = image_path.resize((555, 555))
    #         new_image.save(f"static/img/163/{filename}")
    # image = Image.open("static/img/pesto.jpeg")
    # image.save("static/img/163/pesto_163.jpeg")

            
            

# test()


@app.route('/item/<int:item_id>')
def item(item_id):
    with open("products.json", "r") as file:
        PRODUCTS = json.loads(file.read())
    item = next(i for i in PRODUCTS if i['id'] == item_id)
    return render_template('item.html', item=item)


@app.route('/item/add_to_cart/<int:item_id>')
def add_to_cart(item_id):
    added_pizza = init_added_pizza(item_id)
    if not 'current_order' in session:
        init_cart_cookies(item_id)
    session.modified = True
    cart_list = session['current_order']['items']
    is_pizza_in_order = False
    for cart_item in cart_list:
        if item_id == cart_item['id']:
            is_pizza_in_order = True
            cart_item['quantity'] += 1
            add_notification(f"{added_pizza['name']} WAS ADDED TO CART")
    if is_pizza_in_order == True:
        pass
    else:
        add_item(item_id)
        add_notification(f"{added_pizza['name']} WAS ADDED TO CART")
    return redirect(url_for('index'))


@app.route('/cart/delete_from_cart/<int:item_id>')
def delete_from_cart(item_id):
    added_pizza = init_added_pizza(item_id)
    cart_list = session['current_order']['items']
    for cart_item in cart_list:
        session.modified = True
        if item_id == cart_item['id']:
            add_notification(f"{added_pizza['name']} WAS REMOVED")
            cart_list.remove(cart_item)
    return redirect(url_for('cart'))


@app.route('/cart/remove_one_pizza/<int:item_id>')
def remove_one_pizza(item_id):
    added_pizza = init_added_pizza(item_id)
    cart_list = session['current_order']['items']
    for cart_item in cart_list:
        session.modified = True
        if item_id == cart_item['id']:
            if cart_item['quantity'] > 1:
                cart_item['quantity'] -= 1
                add_notification(f"{added_pizza['name']} WAS REMOVED")
            elif cart_item['quantity'] == 1:
                add_notification(f"{added_pizza['name']} WAS REMOVED")
                cart_list.remove(cart_item)
    return redirect(url_for('cart'))


@app.route('/cart/add_one_pizza/<int:item_id>')
def add_one_pizza(item_id):
    added_pizza = init_added_pizza(item_id)
    cart_list = session['current_order']['items']
    for cart_item in cart_list:
        session.modified = True
        if item_id == cart_item['id']:
            cart_item['quantity'] += 1
            add_notification(f"{added_pizza['name']} WAS ADDED TO CART!")
    return redirect(url_for('cart'))


@app.route('/cart_check')
def cart_check():
    return session['current_order']


@app.route('/cart')
def cart():
    if 'current_order' in session:
        return render_template('cart.html', order=session['current_order'], notifications=get_notifications(), sum=order_sum())
    else:
        return render_template('cart.html', order=[], notifications=get_notifications())


@app.route('/ordering')
def ordering():
    if 'current_order' in session:
        return render_template('ordering.html', order=session['current_order'], notifications=get_notifications(), sum=order_sum())
    else:
        return render_template('ordering.html', order=[], notifications=get_notifications())


@app.route('/create_order', methods=['POST'])
def create_order():
    if request.method == "POST":
        session.modified = True
        with open("orders.json", "r") as file:
            full_order = json.loads(file.read())
        with open("products.json", "r") as file:
            PRODUCTS = json.loads(file.read())
        full_order.append(
            request.form | session['current_order'] |
            {'status': "To do"} | {'date_unix': int(get_time_unix())} | {'date_time': str(get_date_time())})
        print(session['current_order'])
        for order in session['current_order']['items']:
            for product in PRODUCTS:
                if order['id'] == product['id']:
                    product['storage_quantity'] -= order['quantity']
                if product['storage_quantity'] < 0:
                    product['storage_quantity'] = 0
        order_id = 0
        for order in full_order:
            order_id += 1
            order["id"] = order_id
        json_full_order = json.dumps(full_order)
        with open("orders.json", "w") as file:
            file.write(json_full_order)
        json_products_list = json.dumps(PRODUCTS)
        with open("products.json", "w") as file:
            file.write(json_products_list)
        session.clear()
        return redirect("/")
    return render_template('ordering.html', order=session['current_order'])


@app.route('/admin/orders')
def orders():
    filtered_orders = []
    with open("orders.json", "r") as file:
        full_order = json.loads(file.read())
    if request.args.get("order_filter_form"):
        for order in full_order:
            if order["status"] == request.args.get("order_filter_form"):
                filtered_orders.append(order)
        return render_template('orders.html', orders=filtered_orders)
    sorted_full_order = sorted(
        full_order, key=lambda order: order['date_unix'], reverse=True)
    if request.args.get("search_data"):
        for order in full_order:
            if request.args.get("search_data").lower() in order["name"].lower():
                filtered_orders.append(order)
        return render_template('orders.html', orders=filtered_orders)
    return render_template('orders.html', orders=sorted_full_order)


@app.route('/admin/orders/<int:order_id>', methods=["GET", "POST"])
def order(order_id):
    with open("orders.json", "r") as file:
        ORDERS = json.loads(file.read())
    order = next(i for i in ORDERS if i['id'] == order_id)
    if request.method == "POST":
        order["comment"] = request.form["comment"]
    JSON_ORDERS = json.dumps(ORDERS)
    with open("orders.json", "w") as file:
        file.write(JSON_ORDERS)
    return render_template('order.html', order=order)


@app.route('/admin/orders/<int:order_id>/edit', methods=["GET", "POST"])
def edit_order(order_id):
    # if request.methon == "POST":
    with open("orders.json", "r") as file:
        ORDERS = json.loads(file.read())
    order = next(i for i in ORDERS if i['id'] == order_id)
    return render_template('editing_order.html', order=order)


@app.route('/admin/orders/<int:order_id>/edit/save', methods=["POST"])
def save_order(order_id):
    with open("orders.json", "r") as file:
        ORDERS = json.loads(file.read())
    if request.method == "POST":
        session.modified = True
        order = next(
            order for order in ORDERS if order['id'] == order_id)
        order['name'] = request.form["name"]
        order['address'] = request.form["address"]
        order['phone'] = request.form["phone"]
        order['payment_method'] = request.form["payment_method"]
        order["status"] = request.form["status"]
        for item in order['items']:
            if item['name'] == request.form["order_name"]:
                item['quantity'] = request.form["order_quantity"]
        JSON_ORDERS = json.dumps(ORDERS)
        with open("orders.json", "w") as file:
            file.write(JSON_ORDERS)
    return redirect("/admin/orders")


@app.route('/admin/orders/<int:order_id>/status', methods=['POST'])
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


@app.route('/admin')
def admin():
    return render_template('admin_base.html')


@app.route('/admin/products')
def admin_products():
    applied_filter = request.args.get("product_filter_form")
    filtered_products = []
    with open("products.json", "r") as file:
        PRODUCTS = json.loads(file.read())
    if applied_filter:
        for product in PRODUCTS:
            if product["type"] == applied_filter:
                filtered_products.append(product)
        return render_template('products.html', items=filtered_products, applied_filter=applied_filter)
    with open("products.json", "r") as file:
        PRODUCTS = json.loads(file.read())
    return render_template('products.html', items=PRODUCTS, applied_filter=applied_filter)


@app.route('/admin/product/adding_product')
def adding_product():
    return render_template('adding_product.html')


@app.route('/admin/product/adding_product/save', methods=['POST'])
def save_adding_product():
    with open("products.json", "r") as file:
        PRODUCTS = json.loads(file.read())
    if request.method == "POST":
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        session.modified = True
        new_product = {}
        new_product["name"] = request.form["name"]
        new_product["price"] = int(request.form["price"])
        new_product["description"] = request.form["description"]
        new_product["short_description"] = request.form["short_description"]
        new_product["type"] = request.form["type"]
        new_product["id"] = PRODUCTS[-1]['id'] + 1
        new_product["img_src"] = filename
        new_product["display"] = "Off"
        new_product["quantity"] = 1
        new_product["storage_quantity"] = int(request.form["storage_quantity"])
        PRODUCTS.append(new_product)
        json_products_list = json.dumps(PRODUCTS)
        with open("products.json", "w") as file:
            file.write(json_products_list)
    return redirect("/admin/products")


@app.route('/admin/products/<int:product_id>/edit')
def editing_page(product_id):
    with open("products.json", "r") as file:
        PRODUCTS = json.loads(file.read())
    product = next(
        product for product in PRODUCTS if product['id'] == product_id)
    return render_template('editing_product.html', product=product)


@app.route('/admin/products/edit/<int:product_id>/save', methods=['POST'])
def product_save(product_id):
    with open("products.json", "r") as file:
        PRODUCTS = json.loads(file.read())
    if request.method == "POST":
        session.modified = True
        product = next(
            product for product in PRODUCTS if product['id'] == product_id)
        product['name'] = request.form["name"]
        product['price'] = int(request.form["price"])
        product['description'] = request.form["description"]
        product['short_description'] = request.form["short_description"]
        product['display'] = request.form["display"]
        product['img_src'] = request.form["img_src"]
        product['type'] = request.form["type"]
        product["quantity"] = 1
        product['storage_quantity'] = int(request.form["storage_quantity"])
        json_products_list = json.dumps(PRODUCTS)
        with open("products.json", "w") as file:
            file.write(json_products_list)
    return redirect("/admin/products")


@app.route('/admin/products/<int:product_id>/display', methods=['POST'])
def change_display(product_id):
    with open("products.json", "r") as file:
        PRODUCTS = json.loads(file.read())
    if request.method == "POST":
        session.modified = True
        product_to_display = next(
            product for product in PRODUCTS if product['id'] == product_id)
        product_to_display["display"] = request.form["if_display"]
        json_products_list = json.dumps(PRODUCTS)
        with open("products.json", "w") as file:
            file.write(json_products_list)
    return redirect("/admin/products")


@app.route('/admin/products/<int:product_id>/edit', methods=['GET'])
@app.route('/admin/products/<int:product_id>/edit', methods=['POST'])
def add_item(item_id):
    with open("products.json", "r") as file:
        PRODUCTS = json.loads(file.read())
    item = next(i for i in PRODUCTS if i['id'] == item_id)
    item['quantity'] = 1
    session['current_order']['items'].append(item)


def remove_item(item_id):
    with open("products.json", "r") as file:
        PRODUCTS = json.loads(file.read())
    item = next(i for i in PRODUCTS if i['id'] == item_id)
    item['quantity'] = 1
    session['current_order']['items'].remove(item)


def init_cart_cookies(item_id):
    session['current_order'] = {'items': []}


def init_added_pizza(item_id):
    with open("products.json", "r") as file:
        PRODUCTS = json.loads(file.read())
    return next(i for i in PRODUCTS if i['id'] == item_id)


def get_time_unix():
    return time.mktime(datetime.now().timetuple())


def get_date_time():
    return datetime.fromtimestamp(get_time_unix())


def add_notification(message):
    if not 'notifications' in session:
        session['notifications'] = []
    notification = {'message': message, 'time': get_time_unix()}
    session['notifications'].append(notification)


def get_notifications():
    if not 'notifications' in session:
        session['notifications'] = []
    for notification in session['notifications']:
        session.modified = True
        current_time = get_time_unix()
        if int((current_time - 2)) > int(notification['time']):
            session['notifications'].remove(notification)
    return session['notifications']


def order_sum():
    sum = 0
    for item in session['current_order']['items']:
        session.modified = True
        sum += int(item['price'])*item['quantity']
    return sum


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == "__main__":
    app.run(debug=True, port=65432)

