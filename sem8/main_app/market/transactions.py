from datetime import datetime
from typing import TYPE_CHECKING

from database.connection import DBContextManager

if TYPE_CHECKING:
    from database.sql_provider import SQLProvider


class InvalidOrderDataException(Exception):
    "Ошибка неверных входных данных"
    pass


class TransactionProcessor:
    """Класс для выполнения записи заказа в БД."""

    def __init__(self, sql_provider: SQLProvider, db_config: dict) -> None:
        """
        Инициализация класса.

        Args:
            sql_provider - SQLProvider для получения SQL-запросов по их названию
            db_config - Конфиг для подключения к БД
        """
        self.sql_provider: SQLProvider = sql_provider
        self.db_config: dict = db_config

    @staticmethod
    def validate_order(data: dict) -> bool:
        if 'user_id' not in data:
            return False
        if 'basket' not in data:
            return False
        if not data['basket']:
            return False
        for order_item in data['basket']:
            if 'item_id' not in order_item:
                return False
            if 'price' not in order_item:
                return False
            if 'count' not in order_item:
                return False
        return True

    @staticmethod
    def convert_types(data: dict) -> dict:
        if isinstance(data['price'], str):
            data['price'] = float(data['price'])
        if isinstance(data['count'], str):
            data['count'] = int(data['count'])
        return data

    def _create_order_sql(self, data: dict) -> str:
        """
        Создает SQL-запрос для создания заказа в БД.

        Args:
            data - Словарь с описанием заказа
        Returns:
            SQL-запрос для создания заказа
        """

        user_id: str = data['user_id']
        order_dt: str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        order_total_price: int = 0
        order_total_items: int = 0
        for order_item in data['basket']:
            order_item = self.convert_types(order_item)
            order_total_items += order_item['count']
            order_total_price += order_item['count'] * order_item['price']

        return self.sql_provider.get(
            'order.sql',
            dict(
                user_id=user_id,
                order_dt=order_dt,
                order_total_price=order_total_price,
                order_total_items=order_total_items
            )
        )

    def _create_order_details_sql(self, data: dict, order_id: str) -> list[str]:
        """
        Создает SQL-запрос для создания деталей заказа в БД.

        Args:
            data - Словарь с описанием деталей заказа
        Returns:
            Список SQL-запросов для создания описания деталей заказа
        """

        sqls: list[str] = []
        for order_item in data['basket']:
            prod_id = order_item['item_id']
            prod_price = order_item['price']
            prod_count = order_item['count']
            sql = self.sql_provider.get(
                'order_detail.sql',
                dict(
                    order_id=order_id,
                    prod_id=prod_id,
                    prod_price=prod_price,
                    prod_count=prod_count
                )
            )
            sqls.append(sql)
        return sqls

    def make_transaction(self, data: dict) -> str:
        """
        Выполняет транзакцию записи заказа и его описаний в БД.

        Args:
            data - Словарь с описанием деталей заказа
        Returns:
            ID заказа в БД
        """
        if not self.validate_order(data):
            raise InvalidOrderDataException('Invalid order data')

        with DBContextManager(self.db_config, is_transaction=True) as cursor:
            if cursor is None:
                raise ValueError('Cursor is None')

            order_sql = self._create_order_sql(data)
            cursor.execute(order_sql)
            order_id = cursor.lastrowid
            # https://stackoverflow.com/questions/17112852/get-the-new-record-primary-key-id-from-mysql-insert-query

            order_details_sqls = self._create_order_details_sql(data, order_id)
            for order_detail_sql in order_details_sqls:
                cursor.execute(order_detail_sql)

            return order_id
