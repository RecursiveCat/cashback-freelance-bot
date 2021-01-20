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

sql = Sql()
sql.run("SHOW TABLES")
for table in sql.data_base_cursor:
    print(table)
