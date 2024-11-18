import logging


def process():
    while True:
        data = input("Введите математическое выражение или exit для выхода: ")
        if data == "exit":
            return

        try:
            print(eval(data))
        except Exception as e:
            logging.error(f"Произошла ошибка {e}")
