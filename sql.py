import config
import mysql.connector

class Sql:

    def __init__(self):
        self.data_base_connection = mysql.connector.connect(
            host    = config.data_base["host"],
            user    = config.data_base["user"],
            passwd  = config.data_base["password"],
            database= config.data_base["name"]
        )
        self.data_base_cursor = self.data_base_connection.cursor()

    def run(self,query):
        self.data_base_cursor.execute(query)
        self.last_query = query
        return self.data_base_cursor

    def select(self,data,table,condition):
        self.run(f"SELECT {data} FROM {table} {condition}")
        return self.data_base_cursor

    def commit(self):
        self.data_base_connection.commit()
        return self.data_base_cursor

    def get_user_type_by_id(self,id):
        sql.select("type","users",f"WHERE id={id}")
        return self.data_base_cursor

    def get_user_bonuses_by_id(self,id):
        sql.select("bonuses","users",f"WHERE id={id}")
        return self.data_base_cursor

    def get_user_percents_by_id(self,id):
        sql.select("percents","users",f"WHERE id={id}")
        return self.data_base_cursor




"""
функция получения реферов
-
функция получения суммы операции
функция получения бонусов (из операции)
"""

sql = Sql()

for row in sql.get_user_type_by_id(1):
    print(row)
