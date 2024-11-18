import datetime
import logging
import os
import uuid

from jsons import JSONStorage


class Task:
    def __init__(
            self,
            title: str,
            description: str,
            done: bool,
            priority: str,
            due_date: str,
            task_id: str = "",
    ):
        self.task_id = task_id or uuid.uuid4().hex
        self.title = title
        self.description = description
        self.done = done
        self.priority = priority
        self.due_date = due_date

    def __repr__(self):
        return (f"ID: {self.task_id} \n"
                f"Название: {self.title} \n"
                f"Описание: {self.description} \n"
                f"Выполнена: {self.done}\n"
                f"Приоритет: {self.priority}\n"
                f"Срок выполнения: {self.due_date}\n")


class TaskStorage(JSONStorage):
    def __init__(self):
        path = os.getcwd()
        super().__init__(
            os.path.join(path, "data", "tasks.json"),
            Task,
        )

        self.storage = []

    def new(self):
        title = input("Введите краткое описание: ")
        description = input("Введите подробное описание задачи (опционально): ")
        done = bool(input("Введите статус задачи: ") or False)
        priority = input("Введите приоритет: ")
        due_date = input("Введите срок выполнения: ")

        task = Task(title, description, done, priority, due_date)
        self.storage.append(task)

        logging.info("Задача успешно создана")

    def show(self):
        print("Доступные задачи: ")
        for task in self.storage:
            print(task)

    def _get(self, task_id: str) -> Task | None:
        for n in self.storage:
            if n.task_id == task_id:
                return n

        return None

    def complete(self):
        task_id = input("Введите ID: ")
        task = self._get(task_id)

        if not task:
            logging.error("Задача не найдена")
            return

        task.done = True

    def edit(self):
        task_id = input("Введите ID: ")

        task = self._get(task_id)
        if not task:
            logging.error("Задача не найдена")
            return

        title = input("Введите краткое описание: ")
        description = input("Введите подробное описание задачи (опционально): ")
        done = bool(input("Введите статус задачи: ") or False)
        priority = input("Введите приоритет: ")
        due_date = input("Введите срок выполнения: ")

        task.title = title
        task.description = description
        task.done = done
        task.priority = priority
        task.due_date = due_date

        logging.info("Задача успешно изменена")

    def delete(self):
        note_id = input("Введите ID: ")

        note = self._get(note_id)
        if not note:
            logging.error("Задача не найдена")
            return

        self.storage.remove(note)
        logging.info("Задача успешно удалена")


def process():
    text = """
-- Управление задачами --
Выберите действие:
1. Создать задачу
2. Просмотр задач
3. Отметить как выполненную
4. Редактирование задачи
5. Удаление задачи
6. Импорт из файла
7. Экспорт в csv
8. Назад
>>>: """

    _funcs = {
        1: storage.new,
        2: storage.show,
        3: storage.complete,
        4: storage.edit,
        5: storage.delete,
        6: storage.load,
        7: storage.dump,
    }

    while True:
        try:
            user_input = int(input(text))
        except ValueError:
            logging.error("Введите номер действия")
            continue

        if user_input == 8:
            return

        _funcs.get(user_input, lambda *_: print("Номер не найден"))()


storage = TaskStorage()
