from flask import Blueprint, render_template, abort, redirect, url_for, session, request
from data_manipulations import get_products, save_products
from werkzeug.utils import secure_filename
import os
from PIL import Image

admin_products = Blueprint('admin_products', __name__,
                        template_folder='templates')


@admin_products.route('/admin/products')
def admin_products_list():
    applied_filter = request.args.get("product_filter_form")
    filtered_products = []
    products = get_products()
    if applied_filter:
        for product in products:
            if product["type"] == applied_filter:
                filtered_products.append(product)
        return render_template('products.html', items=filtered_products, applied_filter=applied_filter)
    save_products(products)
    return render_template('products.html', items=products, applied_filter=applied_filter)


@admin_products.route('/admin/product/adding_product')
def adding_product():
    return render_template('adding_product.html')


@admin_products.route('/admin/product/adding_product/save', methods=['POST'])
def save_adding_product():
    products = get_products()
    if request.method == "POST":
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(admin_products.config['UPLOAD_FOLDER'], filename))
        print(filename)
        session.modified = True
        new_product = {}
        new_product["name"] = request.form["name"]
        new_product["price"] = int(request.form["price"])
        new_product["description"] = request.form["description"]
        new_product["short_description"] = request.form["short_description"]
        new_product["type"] = request.form["type"]
        new_product["id"] = products[-1]['id'] + 1
        new_product["img_src"] = filename
        new_product["display"] = "Off"
        new_product["quantity"] = 1
        new_product["storage_quantity"] = int(request.form["storage_quantity"])
        products.append(new_product)
        save_products(products)
    image_path = Image.open("static/img/"+filename)
    new_image_163 = image_path.resize((163, 163))
    new_image_333 = image_path.resize((333, 333))
    new_image_555 = image_path.resize((555, 555))   
    new_image_163.save("static/img/163/163_"+filename)
    new_image_333.save("static/img/333/333_"+filename)
    new_image_555.save("static/img/555/555_"+filename)
    os.remove("static/img/"+filename)
    return redirect("/admin/products")


@admin_products.route('/admin/products/<int:product_id>/edit')
def editing_page(product_id):
    products = get_products()
    product = next(
        product for product in products if product['id'] == product_id)
    return render_template('editing_product.html', product=product)


@admin_products.route('/admin/products/edit/<int:product_id>/save', methods=['POST'])
def product_save(product_id):
    products = get_products()
    if request.method == "POST":
        session.modified = True
        product = next(
            product for product in products if product['id'] == product_id)
        product['name'] = request.form["name"]
        product['price'] = int(request.form["price"])
        product['description'] = request.form["description"]
        product['short_description'] = request.form["short_description"]
        product['display'] = request.form["display"]
        product['img_src'] = request.form["img_src"]
        product['type'] = request.form["type"]
        product["quantity"] = 1
        product['storage_quantity'] = int(request.form["storage_quantity"])
        save_products(products)
    return redirect("/admin/products")


@admin_products.route('/admin/products/<int:product_id>/display', methods=['POST'])
def change_display(product_id):
    products = get_products()
    if request.method == "POST":
        session.modified = True
        product_to_display = next(
            product for product in products if product['id'] == product_id)
        product_to_display["display"] = request.form["if_display"]
        save_products(products)
    return redirect("/admin/products")