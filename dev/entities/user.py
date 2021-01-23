import core


class User:

    def __init__(self,telegram_id):
        self.default_bonuses_count = 0
        self.reserved_types = ["customer","seller","operator","admin"]
        if self.valid_telegram_id(telegram_id):
            self.telegram_id = int(telegram_id)
            self.sql = core.Sql()
            self.sql.connect()

    def init(self,type):
            if type in self.reserved_types:
                self.type = type
            self.sql.run("""
            INSERT INTO users(telegram_id,type,bonuses)
            VALUES({},'{}',{});
            """.format(
                self.telegram_id,
                self.type,
                self.default_bonuses_count
            ))
            return self.get_all_data()

    def valid_telegram_id(self,telegram_id):
        if len(str(telegram_id)) != 9:
             print(f"E: invalid telegram id -> {telegram_id}")
        else:
            return True

    def get_all_data(self):
        self.sql.run(f"SELECT * FROM users WHERE telegram_id={self.telegram_id}")
        return self.sql.data_base_cursor


user = User(666712100)
user.init("customer")
print(user.get_all_data())
