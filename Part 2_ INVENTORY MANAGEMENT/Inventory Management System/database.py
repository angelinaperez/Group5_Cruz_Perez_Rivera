import sqlite3

import global_variable as gv


def conn():
    return sqlite3.connect('CROCHET INVENTORY.db')


def add_product(product):
    c = conn()
    cur = c.cursor()
    cur.execute("INSERT or IGNORE INTO product VALUES(null, ?, ?)", product)
    cur.execute("INSERT or IGNORE INTO inventory VALUES(null, 0, ?, ?)", product)
    if cur.rowcount:
        c.commit()
    c.close()


def get_data(table_name_, column_name_='*', filter_='None', filter_value_='None', fetch=''):
    c = conn()
    cur = c.cursor()
    cur.execute(f"SELECT {column_name_} FROM {table_name_}") if filter_ == 'None' \
        else cur.execute(f"SELECT {column_name_} FROM {table_name_} WHERE {filter_} = '{filter_value_}'")
    if fetch == 'all' or filter_ == 'None':
        gv.data = cur.fetchall()
    else:
        gv.data = cur.fetchone()
    c.commit()
    c.close()
    return gv.data


def update(table_name_, set_value, filter_, filter_value_):
    c = conn()
    cur = c.cursor()
    cur.execute(f"UPDATE {table_name_} SET {set_value} WHERE {filter_} = {filter_value_}") if filter_value_ == 'id' \
        else cur.execute(f"UPDATE {table_name_} SET {set_value} WHERE {filter_} = '{filter_value_}'")
    c.commit()
    c.close()


def delete(table_name_, filter_, filter_value_):
    c = conn()
    cur = c.cursor()
    cur.execute(f"DELETE FROM {table_name_} WHERE {filter_} = '{filter_value_}'")
    c.commit()
    c.close()


def purchase(month, year, product):
    c = conn()
    cur = c.cursor()
    cur.execute(f"INSERT INTO '{month} {year} purchase' VALUES(null, ?, ?, ?)", product)

    prev_qty, = get_data(table_name_='inventory', column_name_='stock',
                         filter_='product_name', filter_value_=f'{product[2]}')
    qty = product[1] + prev_qty

    cur.execute(f"UPDATE inventory SET stock = {qty} WHERE product_name = '{product[2]}'")
    c.commit()
    c.close()


def sell(month, year):
    c = conn()
    cur = c.cursor()
    for order in gv.data:
        cur.execute(f"INSERT INTO '{month} {year} sales' VALUES(null, ?, ?, ?, ?, ?, ?)", order)
        c.commit()
    c.close()


def create_table(month, year, window):
    c = conn()
    cur = c.cursor()
    if window == f'PurchaseHistory':
        cur.execute(f"""CREATE TABLE IF NOT EXISTS "{month} {year} purchase" (
                        "id"	INTEGER NOT NULL,
                        "date"	varchar(10) NOT NULL,
                        "QTY"	INTEGER NOT NULL,
                        "product_name"	varchar(50) NOT NULL,
                        PRIMARY KEY("id" AUTOINCREMENT)
                    )""")
    if window == 'Sales':
        cur.execute(f"""CREATE TABLE IF NOT EXISTS "{month} {year} sales" (
                        "id"	INTEGER NOT NULL,
                        "date"	varchar(10) NOT NULL,
                        "customer_name"	varchar(20) NOT NULL,
                        "product_name"	INTEGER NOT NULL,
                        "QTY"	INTEGER NOT NULL,
                        "price"	INTEGER NOT NULL,
                        "amount"	INTEGER NOT NULL,
                        PRIMARY KEY("id" AUTOINCREMENT)
                    )""")
    c.commit()
    c.close()
