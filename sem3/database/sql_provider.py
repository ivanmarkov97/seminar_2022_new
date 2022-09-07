import os

from string import Template


class SQLProvider:
    """Класс для подстановки параметров в SQL-запрос."""

    def __init__(self, file_path: str):
        """
        Инициализурет класс, читает все sql-шаблоны по указаннному пути.

        Args:
            file_path: str - Путь до sql-шаблонов.
        """
        self._scripts = {}
        for file in os.listdir(file_path):
            self._scripts[file] = Template(open(f'{file_path}/{file}').read())

    def get(self, name: str, **kwargs) -> str:
        """
        Выполняет подставновку параметров в указанный sql-шаблон.

        Args:
            name: str - Имя шаблона.
            **kwargs - именвоанные параметры для щаблона.
        """
        return self._scripts.get(name, '').substitute(**kwargs)
