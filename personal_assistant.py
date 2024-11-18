import logging

_funcs = {

}


def main():
    text = """
Добро пожаловать в Персональный помощник!
Выберите действие:
1. Управление заметками
2. Управление задачами
3. Управление контактами
4. Управление финансовыми записями
5. Калькулятор
6. Выход"""

    while True:
        try:
            user_input = int(input())
        except ValueError:
            logging.error("Введите номер действия")
            continue

        _funcs.get(user_input, lambda *_: print("Номер не найден"))


if __name__ == '__main__':
    main()
