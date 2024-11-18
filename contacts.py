import datetime
import logging
import os
import uuid

from jsons import JSONStorage


class Contact:
    def __init__(
            self,
            name: str,
            phone: str,
            email: str,
            contact_id: str = "",
    ):
        self.contact_id = contact_id or uuid.uuid4().hex
        self.name = name
        self.phone = phone
        self.email = email

    def __repr__(self):
        return (f"ID: {self.contact_id} \n"
                f"Имя: {self.name} \n"
                f"Телефон: {self.phone} \n"
                f"Почта: {self.email}\n")


class ContactStorage(JSONStorage):
    def __init__(self):
        path = os.getcwd()
        super().__init__(
            os.path.join(path, "data", "contacts.json"),
            Contact,
        )

        self.storage = []

    def new(self):
        name = input("Введите имя: ")
        phone = input("Введите телефон: ")
        email = input("Введите почту: ")

        task = Contact(name, phone, email)
        self.storage.append(task)

        logging.info("Контакт успешно создан")

    def get(self):
        data = input("Введите имя или номер телефона: ")
        for contact in self.storage:
            if contact.name == data or contact.phone == data:
                print(contact)
                return

        logging.error("Контакт не найден")

    def _get(self, contact_id: str) -> Contact | None:
        for n in self.storage:
            if n.contact_id == contact_id:
                return n

        return None

    def edit(self):
        task_id = input("Введите ID: ")

        task = self._get(task_id)
        if not task:
            logging.error("Контакт не найден")
            return

        name = input("Введите имя: ")
        phone = input("Введите телефон: ")
        email = input("Введите почту: ")

        task.name = name
        task.phone = phone
        task.email = email

        logging.info("Контакт успешно изменен")

    def delete(self):
        note_id = input("Введите ID: ")

        note = self._get(note_id)
        if not note:
            logging.error("Контакт не найден")
            return

        self.storage.remove(note)
        logging.info("Контакт успешно удален")


def process():
    text = """
-- Управление контактами --
Выберите действие:
1. Создать контакт
2. Найтие контакт по имени или номеру
3. Редактирование контакта
4. Удаление контакта
5. Импорт из файла
6. Экспорт в csv
7. Назад
>>>: """

    _funcs = {
        1: storage.new,
        2: storage.get,
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

        if user_input == max(_funcs.keys()) + 1:
            return

        _funcs.get(user_input, lambda *_: print("Номер не найден"))()


storage = ContactStorage()
