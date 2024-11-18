import datetime
import logging
import os
import uuid

from jsons import JSONStorage


class Note:
    def __init__(self, title: str, content: str, timestamp: str, note_id: str = ""):
        self.note_id = note_id or uuid.uuid4().hex
        self.title = title
        self.content = content
        self.timestamp = timestamp

    def __repr__(self):
        return f"ID: {self.note_id}. Title: {self.title}. content: {self.content}"


class NotesStorage(JSONStorage):
    def __init__(self):
        path = os.getcwd()
        super().__init__(
            os.path.join(path, "data", "notes.json"),
            Note,
        )

        self.storage = []

    def new(self):
        title = input("Введите название: ")
        content = input("Введите описание: ")
        timestamp = input("Введите дату: ")

        note = Note(title, content, timestamp)
        self.storage.append(note)

        logging.info("Заметка успешно создана")

    def show(self):
        print("Доступные заметки: ")
        for note in self.storage:
            print(note)

    def _get(self, note_id: str) -> Note | None:
        for n in self.storage:
            if n.note_id == note_id:
                return n

        return None

    def edit(self):
        note_id = input("Введите ID: ")

        note = self._get(note_id)
        if not note:
            print("Заметка не найдена")
            return

        title = input("Введите название: ")
        content = input("Введите описание: ")
        timestamp = input("Введите дату: ")

        note.title = title
        note.content = content
        note.content = content
        note.timestamp = timestamp

        logging.info("Заметка успешно изменена")

    def delete(self):
        note_id = input("Введите ID: ")

        note = self._get(note_id)
        if not note:
            print("Заметка не найдена")
            return

        self.storage.remove(note)
        logging.info("Заметка успешно удалена")


def process():
    text = """
-- Управление заметками --
Выберите действие:
1. Создать заметку
2. Просмотр заметок
3. Редактирование заметки
4. Удаление заметки
5. Импорт из файла
6. Экспорт в csv
7. Назад
>>>: """

    _funcs = {
        1: storage.new,
        2: storage.show,
        3: storage.edit,
        4: storage.delete,
        5: storage.load,
        6: storage.dump,
    }

    while True:
        try:
            user_input = int(input(text))
        except ValueError:
            logging.error("Введите номер действия")
            continue

        if user_input == 7:
            return

        _funcs.get(user_input, lambda *_: print("Номер не найден"))()


storage = NotesStorage()
