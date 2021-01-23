import config
import mysql.connector

OPERATOR_USER = "operator"
COMMON_USER = "customer"
REFER_USER  = "refer"


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


REFERS_SCHEME = [
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

    def bool_checker(self,data):
        count_of_rows = len(list(data))
        if count_of_rows >= 1:
            return True
        else:
            return False

    def user_id_exists(self,id):
        self.select("*","users",f"WHERE id={id}")
        return self.bool_checker(self.data_base_cursor)

    def user_telegram_id_exists(self,telegram_id):
        self.select("*","users",f"WHERE telegram_id={telegram_id}")
        return self.bool_checker(self.data_base_cursor)

    def make_new_user(self,*argv):
        DEFAULT_ARGS = [
          "id","all_bonuses","percent_from_price"
        ]
        if len(USERS_SCHEME)-len(DEFAULT_ARGS) != len(argv):
            print(f"Error: credentials ->{argv} are invalid,"+"""waiting {} getting {}""".format(
              len(USERS_SCHEME)-1,len(argv)
            ))
        elif not self.user_telegram_id_exists(argv[0]):
            query = """
            INSERT INTO users(telegram_id,name,type,all_bonuses,percent_from_price)
              VALUES({},"{}","{}",0,0);
            """.format(argv[0],argv[1],argv[2])
            sql.run(query)
        else:
            print(f"Warning: user with {argv[0]} id already exists")
        return self

    def delete_user_by_telegram_id(self,telegram_id):
        if not self.user_telegram_id_exists(telegram_id):
            print("No such user telegram id in Data Base")
        self.run(f"DELETE FROM users WHERE telegram_id={telegram_id};")
        return self

    def referal_telegram_id_exists(self,refer_telegram_id):
        self.select("*","refers",f"WHERE refer_telegram_id={refer_telegram_id}")
        return self.bool_checker(self.data_base_cursor)

    def make_new_referal(self,*argv):
        if len(REFERS_SCHEME)-1 != len(argv):
            print(f"Error: refer credentials ->{argv} are invalid,"+"""waiting {} getting {}""".format(
              len(REFERS_SCHEME)-1,len(argv)
            ))
        elif not self.referal_telegram_id_exists(argv[0]):
            if self.user_telegram_id_exists(argv[0]):
                query = """
                INSERT INTO refers(refer_telegram_id,customer_telegram_id)
                  VALUES({},{});
                """.format(argv[0],argv[1])
                sql.run(query)
            else:
                print("Warngin: You cannot make non-registered user a referal")
        else:
            print(f"Warning: refer with {argv[0]} id already exists")
        return self

    def get_all_referal_customers(self,referal_telegram_id):
        self.select("*","refers",f"WHERE refer_telegram_id={referal_telegram_id}")
        return self



"""
sql = Sql()
sql.make_new_user(63594,"some_referer",REFER_USER).commit()
sql.make_new_user(17623,"some_customer",COMMON_USER).commit()
sql.make_new_referal(63594,17623).commit()
sql.get_all_referal_customers(63594).print_result()
"""

