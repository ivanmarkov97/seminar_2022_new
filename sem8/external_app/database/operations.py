from typing import Any

from database.connection import DBContextManager


def select(db_config: dict, sql: str) -> tuple[tuple, list[str]]:
    """
    Выполняет запрос (SELECT) к БД с указанным конфигом и запросом.

    Args:
        db_config: dict - Конфиг для подключения к БД.
        sql: str - SQL-запрос.
    Return:
        Кортеж с результатом запроса и описанеим колонок запроса.
    """
    result: tuple = tuple()
    schema: list = []

    with DBContextManager(db_config) as cursor:
        if cursor is None:
            raise ValueError('Cursor not found')

        cursor.execute(sql)
        schema = [column[0] for column in cursor.description]
        result = cursor.fetchall()

    return result, schema


def select_dict(db_config: dict, sql: str) -> list[dict[str, Any]]:
    """
    Выполняет запрос (SELECT) к БД с указанным конфигом и запросом.

    Args:
        db_config: dict - Конфиг для подключения к БД.
        sql: str - SQL-запрос.
    Return:
        Список словарей, где словарь это строка результата sql-запроса.
    """

    rows, schema = select(db_config, sql)
    return [dict(zip(schema, row)) for row in rows]


def call_proc(db_config: dict, proc_name: str, *args: tuple[Any, ...]) -> tuple[Any, ...]:
    """
    Вызываем хранимую процедуру в БД.

    Args:
        db_config: dict - Конфиг для подключения к БД.
        proc_name: str - Название хранимой процедуры.
        *args - Список аргументов хранимой процедуры.
    Return:
        Результат вызова хранимой процедуры.
    """
    with DBContextManager(db_config) as cursor:
        if cursor is None:
            raise ValueError('Cursor not found')
        res = cursor.callproc(proc_name, args)
    return res


def insert_many(db_config: dict, sqls: list[str]) -> int:
    n_insert: int = 0

    with DBContextManager(db_config, is_transaction=True) as cursor:
        if cursor is None:
            raise ValueError('Cursor not found')
        for sql in sqls:
            cursor.execute(sql)
            n_insert += 1
    return n_insert
