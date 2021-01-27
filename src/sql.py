import config
import random
import mysql.connector

"""
TODO:
From me:
[1] Refresh tables
[2] Refresh methods
From cat:
[1] Генерация id с проверкой
[2] Метод для получения реферальных данных по id
[3] Operations schema
"""


class Sql:


    """
    Метод: __init__
    Семантика: Подключение к серверу Базы Даннох
    Принимает: текущий обьект(по умолчанию)
    Возвращает: None
    """
    def __init__(self):
        self.data_base_connection = mysql.connector.connect(
            host    = config.data_base["host"],
            user    = config.data_base["user"],
            passwd  = config.data_base["password"],
            database= config.data_base["name"]
        )
        self.data_base_cursor = self.data_base_connection.cursor()

    """
    Метод: run
    Семантика: запускает SQL запрос
    Принимает: текущий обьект(по умолчанию)
               SQL запрос 
    Возвращает: обьект cursor
    """
    def run(self,query):
        self.data_base_cursor.execute(query)
        return self.data_base_cursor
        
    """
    Метод: commit
    Семантика: сохраняет результат SQL запроса
    Принимает: текущий обьект(по умолчанию)
    Возвращает: None
    """
    def commit(self):
        self.data_base_connection.commit()

    """
    Метод: id_exists_in_table
    Семантика: проверяет, есть ли id в таблице
    Принимает: текущий обьект(по умолчанию)
               имя id
               значение id
               имя таблицы
    Возвращает: True если существует
                False если не существует
    """
    def id_exists_in_table(self,id_name,id,table):
        self.run(f"SELECT * FROM {table} WHERE {id_name}={id}")
        if len(list(self.data_base_cursor)) != 0:
            return True
        else:
            return False

    def create_user_as(self,user_id,name,user_type):

        permission_config = {
            "customer":'FALSE',
            "operator":'FALSE',
            "admin"   :'FALSE'
            }

        if user_type == "customer":
            permission_config["customer"] = 'TRUE'
        elif user_type == "operator":
            permission_config["operator"] = 'TRUE'
        elif user_type == "admin":
            permission_config["admin"] = 'TRUE'


        if not self.id_exists_in_table("id",user_id,"users"):
            self.run("""
            INSERT INTO users(id,name,is_customer,is_operator,is_admin)
            VALUES({},'{}',{},{},{})
            """.format(
                    user_id,
                    name,
                    permission_config["customer"],
                    permission_config["operator"],
                    permission_config["admin"],
                )
            )
            self.commit()
            if self.id_exists_in_table("id",user_id,"users"):
                return True

    def change_permissions_by_uid(self,uid,permission_config):
        sql.run("""
        UPDATE users
        SET is_customer = {},is_operator = {},is_admin = {}
        WHERE id = {};
        """.format(
            permission_config["customer"],
            permission_config["operator"],
            permission_config["admin"],
            uid
        ))
        self.commit()


sql = Sql()
sql.create_user_as(777777777,"zhaba","admin")
sql.change_permissions_by_uid(777777777,
    {
        "customer":"FALSE",
        "operator":"FALSE",
        "admin":"TRUE"
    }
)
