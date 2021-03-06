import psycopg2.extras


def connect_to_db():
    conn = psycopg2.connect("dbname=pizzaritta user=zakharrokishchuk")
    return conn


def disconnect_from_db(conn, cur):
    cur.close()
    conn.close()

    
def get_products():
    conn = connect_to_db()
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cur.execute("select * from products order by id;")
    products = cur.fetchall()
    disconnect_from_db(conn, cur)
    return products


def get_products_to_display():
    conn = connect_to_db()
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cur.execute("select * from products where display = 'On' order by id;")
    products = cur.fetchall()
    disconnect_from_db(conn, cur)
    return products


def get_product(product_id):
    conn = connect_to_db()
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cur.execute(f"select * from products where id = {product_id};")
    product = cur.fetchone()
    disconnect_from_db(conn, cur)
    return product


def filter_products_by_type(type):
    conn = connect_to_db()
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cur.execute(f"select * from products where type = '{type}';")
    products = cur.fetchall()
    disconnect_from_db(conn, cur)
    return products


def filter_products_by_display_type(display_filter):
    query = ""
    if display_filter == "featured":
        query = "select * from products where featured = 'On';"
    elif display_filter == "enabled":
        query = "select * from products where display = 'On';"
    else:
        query = "select * from products where display = 'Off';"
    conn = connect_to_db()
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cur.execute(f"{query}")
    products = cur.fetchall()
    disconnect_from_db(conn, cur)
    return products


def set_product_display(product_id, display):
    conn = connect_to_db()
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cur.execute(f"update products set display = '{display}' where id = {product_id};")
    conn.commit()
    disconnect_from_db(conn, cur)


def set_product_featured(product_id, featured):
    conn = connect_to_db()
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cur.execute(f"update products set featured = '{featured}' where id = {product_id};")
    conn.commit()
    disconnect_from_db(conn, cur)


def update_product(product_id, name, price, description, short_description, display, type, storage_quantity):
    conn = connect_to_db()
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cur.execute(f"""update products set name = '{name}', 
                                        price = '{price}', 
                                        description = '{description}', 
                                        short_description = '{short_description}', 
                                        display = '{display}', 
                                        type = '{type}', 
                                        storage_quantity = '{storage_quantity}'  
                                        where id = {product_id};""")
    conn.commit()
    disconnect_from_db(conn, cur)


def create_product(name, price, description, short_description, display, type, storage_quantity):
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute(f"""insert into products (name, price, description, short_description, display, type, storage_quantity) values (
                                        '{name}', 
                                        '{price}', 
                                        '{description}', 
                                        '{short_description}', 
                                        '{display}', 
                                        '{type}', 
                                        '{storage_quantity}');""")
    conn.commit()
    cur.execute('select max(id) from products')
    product_id = cur.fetchone()
    disconnect_from_db(conn, cur)
    return product_id


def filter_products_by_name(name):
    conn = connect_to_db()
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cur.execute(f"select * from products where name ilike '%{name}%';")
    products = cur.fetchall()
    disconnect_from_db(conn, cur)
    return products


