import config
import random
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
        return self.data_base_cursor

    def commit(self):
        self.data_base_connection.commit()
        return self.data_base_cursor

    def id_exists_in_table(self,id_name,id,table):
        self.run(f"SELECT * FROM {table} WHERE {id_name}={id}")
        if len(list(self.data_base_cursor)) != 0:
            return True
        else:
            return False

    def gen_random_id(self):
        return random.randint(10000,99999)



    def new_user(self,telegram_id,bonuses=0):
        self.run(f"SELECT * FROM users WHERE telegram_id={telegram_id}")
        if(len(list(self.data_base_cursor)) == 0):
            self.run("""
            INSERT INTO users(telegram_id,bonuses)
            VALUES({},{});
            """.format(
                telegram_id,
                bonuses
            ))
            return self

    def delete_user(self,id):
        if self.id_exists_in_table("telegram_id",id,"users"):
            self.run(f"DELETE FROM users WHERE telegram_id={id}")
        return self

    def get_user_bonuses_by_id(self,id):
        if self.id_exists_in_table("telegram_id",id,"users"):
            self.run(f"SELECT bonuses FROM users WHERE telegram_id={id}")
        return int(self.data_base_cursor.fetchall()[0][0])

    def rewrite_user_bonuses(self,id,bonuses):
        if self.id_exists_in_table("telegram_id",id,"users"):
            self.run(f"UPDATE users SET bonuses = {bonuses} WHERE telegram_id = {id};")
            return self



    def new_institution(self,institution_id,name):
        if not self.id_exists_in_table("id",institution_id,"institutions"):
            self.run("""
            INSERT INTO institutions(id,name)
            VALUES({},'{}');
            """.format(institution_id,name))
        return self

    def get_institution_name_by_id(self,id):
        self.run(f"SELECT name FROM institutions WHERE id={id}")
        return str(list(self.data_base_cursor)[0])

    def get_institution_id_by_name(self,name):
        self.run(f"SELECT id FROM institutions WHERE name='{name}'")
        return list(self.data_base_cursor)

    def delete_institution(self,id):
        if self.id_exists_in_table("id",id,"institutions"):
            self.run(f"DELETE FROM institutions WHERE id={id}")
        return self

sql = Sql()
print(sql.get_user_bonuses_by_id(6667121000))
