import os
from string import Template


class SQLProvider:
    """Класс, для получения SQL-запроса по его названию."""

    def __init__(self, file_path: str) -> None:
        """
        Инициализация.

        Args:
             file_path: str - Путь до папки с шаблонами SQL-запросы.
        """

        self._scripts: dict[str, Template] = {}
        for file in os.listdir(file_path):
            self._scripts[file] = Template(open(f'{file_path}/{file}').read())

    def get(self, name: str, kwargs: dict) -> str:
        if name not in self._scripts:
            raise ValueError(f'No such sql-script: {name}')
        return self._scripts.get(name).substitute(**kwargs)
