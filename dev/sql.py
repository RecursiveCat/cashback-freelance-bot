import config
import random
import mysql.connector

"""
TODO:
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

    """
    Метод: create_user_as
    Семантика: создает пользователя
    Принимает: текущий обьект(по умолчанию),
               id пользователя,
               name имя пользователя,
               user_type тип пользователя
    Возвращает: True если пользователь создан
    """
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

    """
    Метод: change_permissions
    Семантика: изменяет права пользователя
    Принимает: текущий обьект(по умолчанию)
               id пользователя
               имя таблицы
    Возвращает: True если существует
                False если не существует
    """
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

    """
    Метод: change_user_name
    Семантика: переписывает имя пользователя по его id
    Принимает: текущий обьект(по умолчанию)
               id пользователя
               name текущее имя
    Возвращает: None 
    """
    def change_user_name(self,uid,name):
        try:
            self.run(f"UPDATE users SET name = '{name}' WHERE id = {uid};")
            self.commit()
        except:
            print("STACK: "+str(__class__)+" -> change_user_name")

    """
    Проверяет является ли передаваемый id - id админа
    """
    def is_admin(self,user_id):
        try:
            sql.run(f"SELECT is_admin FROM users WHERE id = {user_id}")
            return True == (int(list(sql.data_base_cursor)[0][0]))
        except:
            print("STACK: "+str(__class__)+" -> is_admin")

    """
    Метод: make_institution
    Семантика: создает организацию и привязывает к ней админа
    Принимает: self,
               id предприятия
               name предприятия
               id админа (одного из)
    Возвращает: None/True
    """
    def make_institution(self,institution_id,institution_name,admin_id):
        try:
            if self.is_admin(admin_id):
                self.run("""
                INSERT INTO institutions(institution_id,institution_name,admin_id)
                VALUES({},'{}',{});
                """.format(
                    institution_id,
                    institution_name,
                    admin_id
                ))
                self.commit()
                if self.id_exists_in_table("institution_id",institution_id,"institutions"):
                    return True
        except:
            print("STACK: "+str(__class__)+" -> make_institution")

    """
    Метод: bonuses_to_user
    Семантика: зачисляет/отчисляет бонусы пользователю по id
    """
    def bonuses_to_user(self,user_id,bonuses_count,inst_id,do):
        try:
            if self.id_exists_in_table("institution_id",inst_id,"institutions"):
                if self.id_exists_in_table("id",user_id,"users"):
                    if not self.id_exists_in_table("institution_id",inst_id,"bonuses"):
                        self.run("""
                        INSERT INTO bonuses(user_id,bonuses_count,institution_id)
                        VALUES({},{},{});
                        """.format(
                            user_id,
                            bonuses_count,
                            inst_id
                        ))
                        self.commit()
                    else :
                        self.run(f"SELECT bonuses_count FROM bonuses WHERE user_id = {user_id};")
                        all_bonuses_count = int(list(self.data_base_cursor)[0][0])
                        if do == "+":
                            all_bonuses_count = all_bonuses_count + bonuses_count
                        else:
                            all_bonuses_count = all_bonuses_count - bonuses_count
                        self.run(f"UPDATE bonuses SET bonuses_count = {all_bonuses_count} WHERE user_id = {user_id}")
                        self.commit()
        except:
            print("STACK: "+str(__class__)+" -> bonuses_to_user")


    """
    Метод: get_all_user_bonuses_from_inst_id
    Семантика: возвращает все бонусы пользователя в текущей организации
    """
    def get_all_user_bonuses_from_inst_id(self,user_id,inst_id):
        try:
            self.run(f"SELECT bonuses_count FROM bonuses WHERE user_id={user_id} AND institution_id={inst_id}")
            return int(list(self.data_base_cursor)[0][0])
        except:
            print("STACK: "+str(__class__)+" -> get_all_user_bonuses_from_inst_id")

    """
    Метод: gen_random_id
    Генерирует уникальный 5ти значный id 
    """
    def gen_random_id(self):
        cch = random.randint(10000,99999)
        while self.id_exists_in_table("institution_id",cch,"institutions"):
            cch = random.randint(10000,99999)
        return cch

    """
    Метод:  get_all_bonuses_stuff
    Возвращает словари с информацией о бонусах
    """
    def get_all_bonuses_stuff(self,user_id):
        dump = []
        def gen(user_bonuses,inst_name,inst_id):
            return {
                "user_bonuses": user_bonuses,
                "inst_name": inst_name,
                "inst_id": inst_id
            }
        all_users_with_id = list(self.run(f"SELECT * FROM bonuses WHERE user_id = {user_id}"))
        for user in all_users_with_id:
            inst_name = str(list(self.run(f"SELECT institution_name FROM institutions WHERE institution_id={int(user[2])}"))[0][0])
            dump.append(gen(
                int(user[1]),
                str(inst_name),
                int(user[2])
            ))
        return dump



sql = Sql()
print(sql.get_all_user_bonuses_from_inst_id(777777777,77777))
print(sql.get_all_bonuses_stuff(777777777))