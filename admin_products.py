from flask import Blueprint, render_template, redirect, request, current_app
from . import data_manipulations
from werkzeug.utils import secure_filename
import os


admin_products = Blueprint('admin_products', __name__,
                           template_folder='templates')


@admin_products.route('/admin/products')
def admin_products_list():
    product_type = request.args.get("product_filter")
    if product_type:
        return render_template('products.html', items=data_manipulations.filter_products_by_type(product_type), applied_filter=product_type)
    products = data_manipulations.get_products()
    return render_template('products.html', items=products, applied_filter=product_type)


@admin_products.route('/admin/product/adding_product')
def adding_product():
    return render_template('adding_product.html')


@admin_products.route('/admin/product/adding_product/save', methods=['POST'])
def save_added_product():
    products = data_manipulations.get_products()
    new_product = {}
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
    data_manipulations.resize_new_product_picture(filename)
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
    data_manipulations.save_products(products)
    return redirect("/admin/products")


@admin_products.route('/admin/products/<int:product_id>/edit')
def editing_page(product_id):
    return render_template('editing_product.html', product=data_manipulations.get_product(product_id))


@admin_products.route('/admin/products/edit/<int:product_id>/save', methods=['POST'])
def product_save(product_id):
    product = data_manipulations.get_product(product_id)
    product['name'] = request.form["name"]
    product['price'] = int(request.form["price"])
    product['description'] = request.form["description"]
    product['short_description'] = request.form["short_description"]
    product['display'] = request.form["display"]
    product['img_src'] = request.form["img_src"]
    product['type'] = request.form["type"]
    product["quantity"] = 1               # FIXME
    product['storage_quantity'] = int(request.form["storage_quantity"])
    data_manipulations.save_product(product)
    return redirect("/admin/products")


@admin_products.route('/admin/products/<int:product_id>/display', methods=['POST'])
def change_display(product_id):
    product = data_manipulations.get_product(product_id)
    product["display"] = request.form["if_display"]
    data_manipulations.save_product(product)
    return redirect("/admin/products")
