import psycopg2
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
    cur.execute("select orders.id, date_time, user_name, address, phone, payment_method, status, name, quantity from orders inner join order_products on orders.id = order_products.order_id inner join products on order_products.product_id = products.id;")
    orders = cur.fetchall()
    print(orders)
    disconnect_from_db(conn, cur)
    return orders
