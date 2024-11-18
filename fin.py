import datetime
import logging
import os
import uuid

from jsons import JSONStorage


class FinRow:
    def __init__(
            self,
            amount: int,
            category: str,
            date: str,
            description: str,
            fin_id: str = "",
    ):
        self.fin_id = fin_id or uuid.uuid4().hex
        self.amount = amount
        self.category = category
        self.date = date
        self.description = description

    def __repr__(self):
        return (f"ID: {self.fin_id}. "
                f"Сумма: {self.amount}. "
                f"Категория: {self.category}. "
                f"Дата: {self.date}. "
                f"Описание: {self.description}")


class FinRowStorage(JSONStorage):
    def __init__(self):
        path = os.getcwd()
        super().__init__(
            os.path.join(path, "data", "finance.json"),
            FinRow,
        )

        self.storage = []

    def new(self):
        amount = int(input("Введите сумму: "))
        category = input("Введите категорию: ")
        date = input("Введите дату: ")
        description = input("Введите описание: ")

        task = FinRow(amount, category, date, description)
        self.storage.append(task)

        logging.info("Фин. запись успешно создана")

    def get(self):
        date = input("Введите дату для фильтрации (опционально): ")
        category = input("Введите категорию для фильтрации (опционально): ")

        for fin_row in self.storage:
            if (date and fin_row.date == date) and (category and fin_row.category == category):
                print(fin_row)
                continue
            if (date and fin_row.date == date) or (category and fin_row.category == category):
                print(fin_row)
                continue
            if not (date and category):
                print(fin_row)

        logging.error("Фин. запись не найдена")

    def _get(self, fin_id: str) -> FinRow | None:
        for n in self.storage:
            if n.fin_id == fin_id:
                return n

        return None

    def generate(self):
        start_date = datetime.datetime.strptime(input("Введите дату начала: "), "%d-%m-%Y")
        end_date = datetime.datetime.strptime(input("Введите дату окончания: "), "%d-%m-%Y")

        for fin_row in self.storage:
            fin_date = datetime.datetime.strptime(fin_row.date, "%d-%m-%Y")

            if start_date <= fin_date <= end_date:
                print(fin_row)


def process():
    text = """
-- Управление контактами --
Выберите действие:
1. Создать фин. запись
2. Просмотр с фильтрацией
3. Генерация отчета
4. Импорт из файла
5. Экспорт в csv
6. Назад
>>>: """

    _funcs = {
        1: storage.new,
        2: storage.get,
        3: storage.generate,
        4: storage.load,
        5: storage.dump,
    }

    while True:
        try:
            user_input = int(input(text))
        except ValueError:
            logging.error("Введите номер действия")
            continue

        if user_input == max(_funcs.keys()) + 1:
            return

        _funcs.get(user_input, lambda *_: print("Номер не найден"))()


storage = FinRowStorage()
