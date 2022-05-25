import psycopg2
import psycopg2.extras


def connect_to_db():
    conn = psycopg2.connect("dbname=pizzaritta user=zakharrokishchuk")
    return conn


def disconnect_from_db():
    pass

    
def get_products():
    conn = connect_to_db()
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cur.execute("select * from products;")
    products = cur.fetchall()
    return products


def get_products_to_display():
    conn = connect_to_db()
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cur.execute("select * from products where display = 'On';")
    products = cur.fetchall()
    return products


def get_product(product_id):
    conn = connect_to_db()
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cur.execute(f"select * from products where id = {product_id};")
    product = cur.fetchone()
    return product


def filter_products_by_type(type):
    conn = connect_to_db()
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cur.execute(f"select * from products where type = '{type}';")
    products = cur.fetchall()
    return products


def set_product_display(product_id, display):
    conn = connect_to_db()
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cur.execute(f"update products set display = '{display}' where id = {product_id};")
    conn.commit()