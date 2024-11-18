import logging
from notes import process as notes_process, storage as notes_storage
from tasks import process as tasks_process, storage as tasks_storage
from contacts import process as contacts_process, storage as contacts_storage
from fin import process as fin_process, storage as fin_storage


def shutdown():
    for storage in (notes_storage, tasks_storage, contacts_storage, fin_storage):
        storage.dump()


_funcs = {
    1: notes_process,
    2: tasks_process,
    3: contacts_process,
    4: fin_process,
    6: shutdown,
}


def main():
    logging.basicConfig(level=logging.INFO)

    text = """Добро пожаловать в Персональный помощник!
Выберите действие:
1. Управление заметками
2. Управление задачами
3. Управление контактами
4. Управление финансовыми записями
5. Калькулятор
6. Выход
>>> """

    while True:
        try:
            user_input = int(input(text))
        except ValueError:
            logging.error("Введите номер действия")
            continue

        _funcs.get(user_input, lambda *_: print("Номер не найден"))()


if __name__ == '__main__':
    main()
