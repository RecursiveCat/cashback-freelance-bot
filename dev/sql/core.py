"""
 @class core
 Класс используется в качестве ядра, для всех остальных классов,
 которые нужны для взаимодействия с сущностью. Такие как:
 User
"""

import config.DataBase
import mysql.connector


class Sql:

    def connect_with_config_credentials(self):
        self.data_base_connection = mysql.connector.connect(
            host    = DataBase.host,
            user    = DataBase.user,
            passwd  = DataBase.password,
            database= DataBase.name,
        )
        return self

sql = Sql()
sql.connect_with_config_credentials
