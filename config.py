import os

MODE = os.environ.get('MODE')
print('MODE: '+str(MODE))
if MODE == 'test':
    PATH_TO_ORDERS = '/Users/zakharrokishchuk/StudyProject/orders.json'
    PATH_TO_PRODUCTS = '/Users/zakharrokishchuk/StudyProject/tests/fixtures/test_products.json'
    PATH_TO_IMAGES = 'static/img/'
else:
    PATH_TO_ORDERS = '/Users/zakharrokishchuk/StudyProject/orders.json'
    PATH_TO_PRODUCTS = '/Users/zakharrokishchuk/StudyProject/products.json'
    PATH_TO_IMAGES = 'static/img/'

