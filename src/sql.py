import config
import random
import mysql.connector

class Sql:

    """
    Метод: __init__
    Семантика: Подключение к серверу на котором хостится Базы Даннох
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
    """
    def run(self,query):
        self.data_base_cursor.execute(query)
        return self.data_base_cursor
        
    """
    Метод: commit
    Семантика: сохраняет изменения SQL запроса
    в Базе Данных
    """
    def commit(self):
        self.data_base_connection.commit()

    """
    Метод: id_exists_in_table
    Семантика: проверяет, есть ли id в таблице
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
    """
    def change_permissions_by_uid(self,uid,permission_config):
        self.run("""
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
    """
    def change_user_name(self,uid,name):
        self.run(f"UPDATE users SET name = '{name}' WHERE id = {uid};")
        self.commit()


    """
    Метод: get_user_name_by_id
    Вовзращает имя юзера по айди
    """
    def get_user_name_by_id(self,user_id):
        if self.id_exists_in_table("id",user_id,"users"):
            res = list(self.run(f"SELECT name FROM users WHERE id = {user_id}"))
            return str(res[0][0])

    """
    Проверяет является ли передаваемый id - id админа
    """
    def is_admin(self,user_id):
        self.run(f"SELECT is_admin FROM users WHERE id = {user_id}")
        return True == (int(list(self.data_base_cursor)[0][0]))

    """
    Метод: make_institution
    Семантика: создает организацию и привязывает к ней админа
    """
    def make_institution(self,institution_id,institution_name,admin_id):
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


    """
    Проверяет существует ли организация по ее id
    """
    def institution_exists(self,inst_id):
        return self.id_exists_in_table("institution_id",inst_id,"institutions")

    """
    Проверяет существует ли ли юзер по его id
    """
    def user_exists(self,user_id):
        return self.id_exists_in_table("id",user_id,"users")

    """
    Проверяет существует ли связь (юзер + организация) по ее id
    """
    def institution_already_in_node(self,inst_id):
        return self.id_exists_in_table("institution_id",inst_id,"bonuses")

    """
    Проверяет существует ли пользователь хоть в каких-то связях по id
    """
    def user_id_already_in_node(self,user_id):
        return self.id_exists_in_table("user_id",user_id,"bonuses")

    """
    Проверяет существует ли связь по id юзера и организации
    """
    def node_already_exist(self,inst_id,user_id): 
        return self.institution_already_in_node(inst_id) and self.user_id_already_in_node(user_id)

    """
    Проверяет существуют ли все необходимые данные перед созданием связи
    """
    def data_is_valid_before_node_creation(self,user_id,inst_id):
        if  self.institution_exists(inst_id) and self.user_exists(user_id):
            if not self.node_already_exist(inst_id,user_id):
                return True
            else: 
                return False
        else:
            return False

    """
    Метод: bonuses_to_user
    Семантика: зачисляет/отчисляет бонусы пользователю по id
    Использовать только при создании новой связи между заведением
    и пользователем
    """
    def create_operation_node_by_adding_bonuses(self,user_id,bonuses_count,inst_id):
        if self.data_is_valid_before_node_creation(user_id,inst_id):
            sql_query = """INSERT INTO bonuses(user_id,bonuses_count,institution_id) VALUES({},{},{});"""
            self.run(sql_query.format(user_id,bonuses_count,inst_id))
            self.commit()


    """
    Метод: bonuses_to_user
    Использовать только если связь юзера и организации уже
    создана с помощью метода create_operation_node
    """
    def change_user_bonuses(self,user_id,bonuses_count,inst_id):
        self.run(f"UPDATE bonuses SET bonuses_count = {bonuses_count} WHERE user_id = {user_id} AND institution_id = {inst_id}")
        self.commit()

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
    Изменяет проценты скидкы пользователя для организации, чей id передан
    """
    def change_user_sale_percents(self,new_sale_percents,user_id,institution_id):
        sql_query = """UPDATE bonuses SET sale_percents = {} WHERE user_id = {} AND institution_id = {}"""
        self.run(sql_query.format(new_sale_percents,user_id,institution_id))
        self.commit()

    """
    Возвращает проценты скидки пользователя в организации, чей id передан
    """
    def get_user_sale_percents(self,user_id,institution_id):
        sql_query = f"SELECT sale_percents FROM bonuses WHERE user_id = {user_id} AND institution_id = {institution_id}"
        query_result = self.run(sql_query)
        readable_result = int(list(query_result)[0][0])
        return readable_result


    """
    Метод:  get_all_bonuses_stuff
    Возвращает словари с информацией о бонусах
    """
    def get_all_bonuses_stuff(self,user_id):
        dump = []
        def gen(user_bonuses,inst_name,inst_id):
            return {
                "user" : {
                    "id": user_id,
                    "name": self.get_user_name_by_id(user_id),
                    "bonuses": user_bonuses,
                },
                "institution": {
                    "name": inst_name,
                    "id": inst_id
                }
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




