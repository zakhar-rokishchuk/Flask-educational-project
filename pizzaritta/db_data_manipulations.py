import psycopg2
import psycopg2.extras


def connect_to_db():
    conn = psycopg2.connect("dbname=pizzaritta user=zakharrokishchuk")
    return conn

    
def get_products():
    conn = connect_to_db()
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cur.execute("select * from products;")
    products = cur.fetchall()
    return products

def get_new_product_id():
    conn = connect_to_db()
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)   
    cur.execute("select max(id) as max_id from products;")
    id = cur.fetchone()['max_id']
    new_product_id = id + 1 if id else 1
    return new_product_id


    # orders = get_orders()
    # if not orders[-1]['id']:
    #     new_order_id = 1
    # new_order_id = orders[-1]['id'] + 1
    # return new_order_id


def get_products_to_display():
    products = get_products()
    products_to_display = []
    for product in products:
        if product["display"] == "On":
            products_to_display.append(product)
    return products_to_display
