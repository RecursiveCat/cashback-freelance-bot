"""
@class core
Класс используется в качестве ядра, для всех остальных классов,
которые нужны для взаимодействия с сущностью. Такие как:
Customer,Operator,Admin - все это интерфейсы для взаимодействия
с Базой Данных
"""

import config
import mysql.connector
from config import DataBaseSettings


class Sql:

    def connect(self):
        """
        Подключает клиент к Базе Данных используя даныные из файла
        ./app/sql/config.py
         """
        self.data_base_connection = mysql.connector.connect(
            host    = DataBaseSettings.host,
            user    = DataBaseSettings.user,
            passwd  = DataBaseSettings.password,
            database= DataBaseSettings.name,
        )
        self.data_base_cursor = self.data_base_connection.cursor()
        return self

    def run(self,query):
        """
        Метод нужен для написания более компактных запросов
        которые обрабатываются на наличие ошибок
        """
        self.data_base_cursor.execute(query)
        return self.data_base_cursor
        print(f"E: cannot run sql query :\n{query}")

    def result(self):
        return self.data_base_cursor

    def commit(self):
        """
        Метод нужен для сохранения изменений в Базе Данных:
        будь то удаление, перезапись старых или запись новых
        данных
        """
        return self.data_base_connection.commit()

    def close(self):
        """
        Метод закрывает текущее соединение с БД
        """
        return self.data_base_connection.close()



