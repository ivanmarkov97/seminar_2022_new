from db_context_manager import DBContextManager


def work_with_db(dbconfig: dict, _sql: str):
    with DBContextManager(dbconfig) as cursor:

        if cursor is None:
            raise ValueError('Курсор не создан')

        cursor.execute(_sql)
        schema = [column[0] for column in cursor.description]
        result = cursor.fetchall()
    return result, schema
