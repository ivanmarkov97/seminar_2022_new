from DBcm import UseDatabase


def work_with_db(dbconfig: dict, sql: str):
    with UseDatabase(dbconfig) as cursor:

        if cursor is None:
            raise ValueError('Курсор не создан')

        cursor.execute(sql)
        schema = [column[0] for column in cursor.description]
        result = cursor.fetchall()
    return result, schema
