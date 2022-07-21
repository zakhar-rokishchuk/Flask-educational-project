from flask import Blueprint, render_template, redirect, request
from . import db_products_manipulations
from . import image_tools


admin_products = Blueprint('admin_products', __name__,
                           template_folder='templates')


@admin_products.route('/admin/products')
def admin_products_list():
    product_type = request.args.get('product_type_filter')
    display_type = request.args.get('product_display_filter')
    search_name = request.args.get("search_name")
    if display_type:
        return render_template('products.html', items=db_products_manipulations.filter_products_by_display_type(display_type), applied_display_filter=display_type)
    elif product_type:
        return render_template('products.html', items=db_products_manipulations.filter_products_by_type(product_type), applied_type_filter=product_type)
    elif search_name:
        print(search_name)
        return render_template('products.html', items=db_products_manipulations.filter_products_by_name(search_name))
    products = db_products_manipulations.get_products()
    return render_template('products.html', items=products, applied_type_filter=product_type, applied_display_filter=display_type)


@admin_products.route('/admin/product/adding_product')
def adding_product():
    return render_template('adding_product.html')


@admin_products.route('/admin/product/adding_product/save', methods=['POST'])
def save_added_product():
    product_id = db_products_manipulations.create_product(request.form["name"], 
                                                          int(request.form["price"]), 
                                                          request.form["description"], 
                                                          request.form["short_description"], 
                                                          request.form["display"], 
                                                          request.form["type"], 
                                                          int(request.form["storage_quantity"]))
    image_tools.generate_pictures(request.files['file'], *product_id)
    return redirect('/admin/products')


@admin_products.route('/admin/products/<int:product_id>/edit')
def editing_product(product_id):
    return render_template('editing_product.html', product=db_products_manipulations.get_product(product_id))


@admin_products.route('/admin/products/edit/<int:product_id>/save', methods=['POST'])
def save_updated_product(product_id):
    db_products_manipulations.update_product(product_id, 
                                             request.form["name"], 
                                             int(request.form["price"]), 
                                             request.form["description"], 
                                             request.form["short_description"], 
                                             request.form["display"], 
                                             request.form["type"], 
                                             int(request.form["storage_quantity"]))
    image_tools.generate_pictures(request.files['file'], product_id)
    return redirect('/admin/products')


@admin_products.route('/admin/products/<int:product_id>/display', methods=['POST'])
def change_display(product_id):
    db_products_manipulations.set_product_display(product_id, request.form["if_display"])
    return redirect('/admin/products')


@admin_products.route('/admin/products/<int:product_id>/featured', methods=['POST'])
def change_featured(product_id):
    db_products_manipulations.set_product_featured(product_id, request.form["if_featured"])
    return redirect('/admin/products')
