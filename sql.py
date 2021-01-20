import config
import mysql.connector

OPERATIONS_SCHEME = [
             "price_from_user_telegram_id",
             "price_to_user_telegram_id",
             "bonuses_to_user_telegram_id",
             "bonuses_count",
             "only_bonuses",
             "percent_from_price",
             "price",
]

USERS_SCHEME = [
             "id",
             "telegram_id",
             "name",
             "type",
             "all_bonuses",
             "percent_from_price",
]

REFERS_SHEME = [
             "id",
             "refer_telegram_id",
             "customer_telegram_id",
]

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

    def select(self,data,table,condition=None):
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

    def get_referal_id_by_id(self,id):
        sql.select("refer_telegram_id","refers",f"WHERE id={id}")
        return self.data_base_cursor

    def get_operation_price_by_id(self,id):
        sql.select("price","operations")
        return self.data_base_cursor

    def get_operation_bonuses_by_id(self,id):
        sql.select("bonuses_count","operations",f"WHERE id={id}")
        return self.data_base_cursor

    def get_operation_money_to_user_telegram_id_by_id(self,id):
        sql.select("price_to_user_telegram_id","operations",f"WHERE id={id}")
        return self.data_base_cursor

    def get_operation_bonuses_to_user_telegram_id_by_id(self,id):
        sql.select("bonuses_to_user_telegram_id","operations",f"WHERE id={id}")
        return self.data_base_cursor

    def print_result(self):
        for row in self.data_base_cursor:
            print(row)


"""
sql = Sql()
sql.run("SHOW TABLES")
sql.print_result()
sql.select("*","users")
sql.print_result()
sql.get_user_type_by_id(1)
sql.print_result()
sql.get_user_all_bonuses_by_id(1)
sql.print_result()
sql.get_user_percent_from_price_by_id(1)
sql.print_result()
sql.get_user_name_by_id(1)
sql.print_result()
sql.get_user_tg_id_by_id(1)
sql.print_result()
sql.get_referal_id_by_id(1)
sql.print_result()
sql.get_operation_price_by_id(1)
sql.print_result()
sql.get_operation_bonuses_by_id(1)
sql.print_result()
sql.get_operation_money_to_user_telegram_id_by_id(1)
sql.print_result()
sql.get_operation_bonuses_to_user_telegram_id_by_id(1)
sql.print_result()
"""
