from flask import Flask
from . import site_catalog
from . import site_cart
from . import admin_orders
from . import admin_products

def create_app():
    app = Flask(__name__)

    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    UPLOAD_FOLDER = 'static/img'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.secret_key = b'SAJGDD&S^ATDIGU^%)_'

    app.register_blueprint(site_catalog.site_catalog)
    app.register_blueprint(site_cart.site_cart)
    app.register_blueprint(admin_orders.admin_orders)
    app.register_blueprint(admin_products.admin_products)

    # if __name__ == "__main__":
        # app.run(debug=True, port=65432)

    return app

