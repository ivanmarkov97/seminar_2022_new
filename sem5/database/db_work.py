from typing import Tuple, List

from sem3.database.db_context_manager import DBContextManager


def select(db_config: dict, sql: str) -> Tuple[Tuple, List[str]]:
    """
    Выполняет запрос (SELECT) к БД с указанным конфигом и запросом.

    Args:
        db_config: dict - Конфиг для подключения к БД.
        sql: str - SQL-запрос.
    Return:
        Кортеж с результатом запроса и описанеим колонок запроса.
    """
    result: tuple = tuple()
    schema: list[str] = []

    with DBContextManager(db_config) as cursor:
        if cursor is None:
            raise ValueError('Cursor not found')

        cursor.execute(sql)
        schema = [column[0] for column in cursor.description]
        result = cursor.fetchall()

    return result, schema


def select_dict(db_config: dict, sql: str) -> list[dict]:
    """
    Выполняет запрос (SELECT) к БД с указанным конфигом и запросом.

    Args:
        db_config: dict - Конфиг для подключения к БД.
        sql: str - SQL-запрос.
    Return:
        Список словарей, где словарь это строка результата sql-запроса.
    """

    with DBContextManager(db_config) as cursor:

        if cursor is None:
            raise ValueError('Cursor not found')

        cursor.execute(sql)
        result: list[dict] = []
        schema: list[str] = [column[0] for column in cursor.description]

        for row in cursor.fetchall():
            result.append(dict(zip(schema, row)))

        return result


def call_proc(db_config: dict, proc_name: str, *args) -> tuple:
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
        res: tuple = cursor.callproc(proc_name, args)
        return res
