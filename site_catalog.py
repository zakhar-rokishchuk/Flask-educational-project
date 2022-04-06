from flask import Blueprint, render_template, abort
from data_manipulations import get_products, save_products, get_product, get_products_to_display, get_orders, save_orders, get_order
from notifications import get_notifications


site_catalog = Blueprint('site_catalog', __name__,
                        template_folder='templates')


@site_catalog.route('/')
def index():
    products_to_display = get_products_to_display()
    return render_template('index.html', items=products_to_display, notifications=get_notifications())


@site_catalog.route('/item/<int:item_id>')
def item(item_id):
    item = get_product(item_id)
    return render_template('item.html', item=get_product(item_id))
