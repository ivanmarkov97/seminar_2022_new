from __future__ import annotations

from typing import TYPE_CHECKING

from pymysql import connect

if TYPE_CHECKING:
    from pymysql.connections import Connection
    from pymysql.cursors import Cursor


def create_database(db_config: dict) -> None:
    """Создает базу данных supermarket."""

    conn: Connection = connect(**db_config)
    cursor: Cursor = conn.cursor()

    db_name: str = 'supermarket'

    # create database
    cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")
    cursor.execute(f"CREATE DATABASE {db_name}")
    conn.commit()

    create_tables(cursor, db_name)
    conn.commit()

    insert_data(cursor, db_name)
    conn.commit()

    cursor.close()
    conn.close()


def create_tables(cursor: Cursor, db_name: str) -> None:
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {db_name}.product (
        prod_id INT NOT NULL AUTO_INCREMENT,
        prod_name VARCHAR(32) NOT NULL,
        prod_price DECIMAL(7, 2) NOT NULL CHECK (prod_price >= 0),
        prod_measure INT UNSIGNED CHECK (prod_measure >= 0),
        PRIMARY KEY (prod_id)
    )
    """)

    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {db_name}.internal_user (
        user_id INT NOT NULL AUTO_INCREMENT,
        user_group VARCHAR(32) NOT NULL,
        login VARCHAR(64) NOT NULL,
        password VARCHAR(64) NOT NULL,
        PRIMARY KEY (user_id)
    )
    """)

    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {db_name}.external_user (
        user_id INT NOT NULL AUTO_INCREMENT,
        login VARCHAR(64) NOT NULL,
        password VARCHAR(64) NOT NULL,
        PRIMARY KEY (user_id)
    )
    """)

    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {db_name}.orders (
        order_id INT NOT NULL AUTO_INCREMENT,
        order_dt DATETIME NOT NULL,
        order_total_price DECIMAL(8, 2) NOT NULL CHECK (order_total_price > 0.0),
        order_total_items INT UNSIGNED NOT NULL CHECK (order_total_items > 0),
        user_id INT NOT NULL,
        PRIMARY KEY (order_id),
        FOREIGN KEY (user_id) REFERENCES {db_name}.external_user (user_id)
    )
    """)

    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {db_name}.order_details (
        order_detail_id INT NOT NULL AUTO_INCREMENT,
        order_id INT NOT NULL,
        prod_id INT NOT NULL,
        prod_price DECIMAL(7, 2) NOT NULL CHECK (prod_price > 0.0),
        prod_count INT UNSIGNED NOT NULL CHECK (prod_count > 0),
        PRIMARY KEY (order_detail_id),
        FOREIGN KEY (order_id) REFERENCES {db_name}.orders (order_id),
        FOREIGN KEY (prod_id) REFERENCES {db_name}.product (prod_id)
    )
    """)


def insert_data(cursor: Cursor, db_name: str) -> None:
    # product
    products: list[dict] = [
        {'prod_name': 'рубашка', 'prod_price': 1000, 'prod_measure': 10},
        {'prod_name': 'джинсы', 'prod_price': 2000, 'prod_measure': 20},
        {'prod_name': 'куртка', 'prod_price': 5000, 'prod_measure': 5},
        {'prod_name': 'рюкзак', 'prod_price': 1500, 'prod_measure': 10},
        {'prod_name': 'майка', 'prod_price': 500, 'prod_measure': 12},
        {'prod_name': 'футболка', 'prod_price': 1500, 'prod_measure': 3},

        {'prod_name': 'банан', 'prod_price': 300, 'prod_measure': 30},
        {'prod_name': 'апельсин', 'prod_price': 350, 'prod_measure': 40},
        {'prod_name': 'мясо', 'prod_price': 1000, 'prod_measure': 45},
        {'prod_name': 'творог', 'prod_price': 400, 'prod_measure': 20},
        {'prod_name': 'вода', 'prod_price': 100, 'prod_measure': 21},
    ]

    sql: str = f"""
    INSERT INTO {db_name}.product (prod_id, prod_name, prod_price, prod_measure)
    VALUES (NULL, %(prod_name)s, %(prod_price)s, %(prod_measure)s)
    """
    cursor.executemany(sql, products)

    # internal_user
    internal_users: list[dict] = [
        {'user_group': 'typical', 'login': 'user_typical', 'password': 'password_typical'},
        {'user_group': 'admin', 'login': 'user_admin', 'password': 'password_admin'},
    ]

    sql: str = f"""
    INSERT INTO {db_name}.internal_user (user_id, user_group, login, password)
    VALUES (NULL, %(user_group)s, %(login)s, %(password)s)
    """
    cursor.executemany(sql, internal_users)
    cursor.execute(f"SELECT * FROM {db_name}.internal_user")

    # external_user
    external_users: list[dict] = [
        {'login': 'user_1', 'password': 'password_1'},
        {'login': 'user_2', 'password': 'password_2'},
        {'login': 'user_3', 'password': 'password_3'},
    ]

    sql: str = f"""
    INSERT INTO {db_name}.external_user (user_id, login, password)
    VALUES (NULL, %(login)s, %(password)s)
    """
    cursor.executemany(sql, external_users)

    # orders
    orders: list[dict] = [
        {'order_dt': '2024-08-10 12:00:00', 'order_total_price': '1000', 'order_total_items': '1', 'user_id': '1'},
    ]

    sql: str = f"""
    INSERT INTO {db_name}.orders (order_id, order_dt, order_total_price, order_total_items, user_id)
    VALUES (NULL, %(order_dt)s, %(order_total_price)s, %(order_total_items)s, %(user_id)s)
    """
    cursor.executemany(sql, orders)

    # order_details
    order_details: list[dict] = [
        {'order_id': '1', 'prod_id': '1', 'prod_price': 1000, 'prod_count': 1}
    ]

    sql: str = f"""
    INSERT INTO {db_name}.order_details (order_detail_id, order_id, prod_id, prod_price, prod_count)
    VALUES (NULL, %(order_id)s, %(prod_id)s, %(prod_price)s, %(prod_count)s)
    """
    cursor.executemany(sql, order_details)


if __name__ == '__main__':
    create_database({
        'host': '127.0.0.1',
        'port': 3307,
        'user': 'root',
        'password': 'root'
    })
