import psycopg2.extras


def connect_to_db():
    conn = psycopg2.connect("dbname=pizzaritta user=zakharrokishchuk")
    return conn


def disconnect_from_db(conn, cur):
    cur.close()
    conn.close()


def get_orders():
    conn = connect_to_db()
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cur.execute(f"select * from orders order by date_time desc;")
    orders = cur.fetchall()
    disconnect_from_db(conn, cur)
    return orders


def get_order(order_id):
    conn = connect_to_db()
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cur.execute(f"select * from orders where id = '{order_id}';")
    order = cur.fetchall()
    cur.execute(f"""select products.id, products.name, order_products.quantity from order_products 
                    inner join products on order_products.product_id = products.id 
                    where order_products.order_id = '{order_id}';""")
    order_items = cur.fetchall()
    return order, order_items


def filter_orders_by_status(status):
    conn = connect_to_db()
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cur.execute(f"select * from orders where status = '{status}';")
    orders = cur.fetchall()
    disconnect_from_db(conn, cur)
    return orders


def filter_orders_by_name(name):
    conn = connect_to_db()
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cur.execute(f"select * from orders where user_name ilike '%{name}%';")
    orders = cur.fetchall()
    disconnect_from_db(conn, cur)
    return orders


def add_comments(order_id, comments):
    conn = connect_to_db()
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cur.execute(f"update orders set comments = '{comments}' where id = '{order_id}' ;")
    conn.commit()
    disconnect_from_db(conn, cur)


def change_status(order_id, status):
    conn = connect_to_db()
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cur.execute(f"update orders set status = '{status}' where id = '{order_id}' ;")
    conn.commit()
    disconnect_from_db(conn, cur)


def update_order(order_id, date_time, user_name, address, phone, payment_method, status):
    conn = connect_to_db()
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cur.execute(f"""update orders set date_time = '{date_time}', 
                                      user_name = '{user_name}', 
                                      address = '{address}', 
                                      phone = '{phone}', 
                                      payment_method = '{payment_method}', 
                                      status = '{status}' 
                                      where id = '{order_id}';""")
    conn.commit()
    disconnect_from_db(conn, cur)


def update_order_product_quantity(order_id, product_id, quantity):
    conn = connect_to_db()
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cur.execute(f"update order_products set quantity = '{quantity}' where order_id = '{order_id}' and product_id = '{product_id}';")
    conn.commit()
    disconnect_from_db(conn, cur)
