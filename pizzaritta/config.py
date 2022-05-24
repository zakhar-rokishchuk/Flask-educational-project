from os import path, environ
from dotenv import load_dotenv


ROOT_DIR = path.abspath(path.dirname(path.dirname(__file__)))
load_dotenv(path.join(ROOT_DIR, '.env'))
database_config = {
    'user': environ.get('DB_USERNAME'),
    'password': environ.get('DB_PASSWORD'),
    'host': environ.get('DB_HOST'),
    'port': environ.get('DB_PORT'),
    'database': environ.get('DB_DATABASE')
}


MODE = environ.get('MODE')
if MODE == 'test':
    PATH_TO_ORDERS = '/Users/zakharrokishchuk/StudyProject/orders.json'
    PATH_TO_PRODUCTS = '/Users/zakharrokishchuk/StudyProject/tests/fixtures/test_products.json'
    PATH_TO_IMAGES = 'static/img/'
else:
    PATH_TO_ORDERS = '/Users/zakharrokishchuk/StudyProject/pizzaritta/orders.json'
    PATH_TO_PRODUCTS = '/Users/zakharrokishchuk/StudyProject/pizzaritta/products.json'
    PATH_TO_IMAGES = f'{ROOT_DIR}/pizzaritta/static/img/'

