from __future__ import annotations
from typing import TYPE_CHECKING

from loguru import logger
from pymysql import connect
from pymysql.err import OperationalError


if TYPE_CHECKING:
    from types import TracebackType

    from pymysql.cursors import Cursor
    from pymysql.connections import Connection


class DBContextManager:
    """Класс для подключения к БД и выполнения sql-запросов."""

    def __init__(self, config: dict) -> None:
        """
        Инициализация объекта подключения.

        Args:
             config: dict - Конфиг дял подключения к БД.
        """
        self.config: dict = config
        self.conn: Connection | None = None
        self.cursor: Cursor | None = None

    def __enter__(self) -> Cursor | None:
        """
        Реализует логику входа в контекстный менеджер.
        Создает соединение к БД и возвращает курсор для выполнения запросов.

        Return:
            Курсор для работы с БД или NULL.
        """
        try:
            self.conn = connect(**self.config)
            self.cursor = self.conn.cursor()
            return self.cursor

        except OperationalError as err:
            if err.args[0] == 1045:
                logger.error('Invalid login or password')
            elif err.args[0] == 1049:
                logger.error('Check database name')
            else:
                logger.error(str(err))
            return None

    def __exit__(
            self,
            exc_type: type | None,
            exc_val: ValueError | None,
            exc_tr: TracebackType | None
    ) -> bool:
        """
        Реализует логику выхода из контекстого менеджера для работы с БД.
        Закрывает соединение и курсор.
        Возвращаемое значение всего True для обеспечения сокрытия списка ошибок в консоли.

        Args:
            exc_type: Тип возможной ошибки при работе менеджера.
            exc_val: Значение возможной ошибки при работе менеджера.
            exc_tr: Traceback (подробный текст ошибки) при работе менеджера.
        """

        if self.conn and self.cursor:
            if exc_type:
                logger.error('Invalid DB operation. Rollback')
                self.conn.rollback()
            else:
                self.conn.commit()
            self.conn.close()
            self.cursor.close()
        return True
