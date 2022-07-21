from flask import Flask
from . import site_catalog
from . import site_cart
from . import admin_orders
from . import admin_products
from . import login

def create_app():
    app = Flask(__name__)

    UPLOAD_FOLDER = 'static/img'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.secret_key = b'SAJGDD&S^ATDIGU^%)_'

    app.register_blueprint(site_catalog.site_catalog)
    app.register_blueprint(site_cart.site_cart)
    app.register_blueprint(admin_orders.admin_orders)
    app.register_blueprint(admin_products.admin_products)
    app.register_blueprint(login.login)

    return app
