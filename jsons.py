import json
import logging
import os.path


class JSONStorage:
    def __init__(self, path: str, storage_object: type):
        self.path = path
        self.storage_object = storage_object
        self.storage = []
        pass

    def dump(self):
        with open(self.path, "w", encoding="utf-8") as file:
            json.dump([obj.__dict__ for obj in self.storage], file)

        logging.info(f"{self.storage_object.__name__} успешно сохранен в {self.path}")

    def load(self):
        with open(self.path, "r", encoding="utf-8") as file:
            self.storage = [self.storage_object(**data) for data in json.load(file)]

        logging.info("Успешно")

