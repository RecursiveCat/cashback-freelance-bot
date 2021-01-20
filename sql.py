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

    def get_user_all_bonuses_by_id(self,id):
        sql.select("all_bonuses","users",f"WHERE id={id}")
        return self.data_base_cursor

    def get_user_percent_from_price_by_id(self,id):
        sql.select("percent_from_price","users",f"WHERE id={id}")
        return self.data_base_cursor

    def get_user_name_by_id(self,id):
        sql.select("name","users",f"WHERE id={id}")
        return self.data_base_cursor

    def get_user_tg_id_by_id(self,id):
        sql.select("telegram_id","users",f"WHERE id={id}")
        return self.data_base_cursor



"""
функция получения реферов
-
функция получения суммы операции
функция получения бонусов (из операции)
"""

sql = Sql()
"""
sql.run(INSERT INTO users(telegram_id,name,type,all_bonuses,percent_from_price)
           VALUES (1923891389,"zhaba","customer",5,1);)
"""

for row in sql.get_user_type_by_id(1):
    print(row)

for row in sql.get_user_tg_id_by_id(1):
    print(row)

for row in sql.get_user_name_by_id(1):
    print(row)

for row in sql.get_user_percent_from_price_by_id(1):
    print(row)

for row in sql.get_user_all_bonuses_by_id(1):
    print(row)

