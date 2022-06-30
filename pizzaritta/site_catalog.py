from flask import Blueprint, render_template
from . import notifications
from . import db_products_manipulations


site_catalog = Blueprint('site_catalog', __name__,
                        template_folder='templates')


@site_catalog.route('/')
def index():
    products_to_display = db_products_manipulations.get_products_to_display()
    return render_template('index.html', items=products_to_display, notifications=notifications.get_notifications())


@site_catalog.route('/item/<int:item_id>')
def item(item_id):
    return render_template('item.html', item=db_products_manipulations.get_product(item_id))
