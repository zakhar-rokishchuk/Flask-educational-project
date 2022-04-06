from flask import Flask
from data_manipulations import get_products, save_products, get_product, get_products_to_display, get_orders, save_orders, get_order
from notifications import get_notifications, add_notification
from site_catalog import site_catalog
from site_cart import site_cart
from admin_orders import admin_orders
from admin_products import admin_products


app = Flask(__name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = 'static/img'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = b'SAJGDD&S^ATDIGU^%)_'

app.register_blueprint(site_catalog)
app.register_blueprint(site_cart)
app.register_blueprint(admin_orders)
app.register_blueprint(admin_products)

if __name__ == "__main__":
    app.run(debug=True, port=65432)
