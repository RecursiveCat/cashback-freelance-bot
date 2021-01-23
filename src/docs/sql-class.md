```
[1] Class Sql
    var data_base_connection
    var data_base_cursor
    var last_query
    OPERATOR_USER 
    COMMON_USER 
    REFER_USER 
    OPERATIONS_SCHEME
    USERS_SCHEME
    REFERS_SCHEME 
    def __init__(self)
    def run(self,query)
    def select(self,data,table,condition=None)
    def commit(self)
    def get_user_type_by_id(self,id)
    def get_user_all_bonuses_by_id(self,id)
    def get_user_percent_from_price_by_id(self,id)
    def get_user_name_by_id(self,id)
    def get_user_tg_id_by_id(self,id)
    def delete_user_by_telegram_id(self,telegram_id) 
    def get_referal_id_by_id(self,id)
    get_all_referal_customers(self,id)
    def referal_telegram_id_exists(self,refer_telegram_id)
    def make_new_referal(self,*argv)
    def get_operation_price_by_id(self,id)
    def get_operation_bonuses_by_id(self,id)
    def get_operation_money_to_user_telegram_id_by_id(self,id)
    def get_operation_bonuses_to_user_telegram_id_by_id(self,id) 
    def print_result(self) -> void
    def save_new_user(17623373393,"test_refer3","refer3",123,2) -> self
    def user_id_exists(5))
    def user_telegram_id_exists(1923891386)
```


Examlpe 1 :
```
sql = Sql()
sql.run("SHOW TABLES")
sql.print_result()
sql.select("*","users")
sql.print_result()
sql.get_user_type_by_id(1)
sql.print_result()
def get_referal_id_by_id(self,id)
sql.get_user_all_bonuses_by_id(1)
sql.print_result()
sql.get_user_percent_from_price_by_id(1)
sql.print_result()
sql.get_user_name_by_id1)
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
```

Result:
```
('operations',)
('refers',)
('users',)
(1, 1923891389, 'zhaba', 'customer', 5, 1)
(2, 1923891389, 'zhaba', 'customer', 5, 1)
(3, 1923891389, 'zhaba', 'customer', 5, 1)
(8, 8394321923, 'recuirsive_cat', 'customer', 2, 1)
('customer',)
(5,)
(1,)
('zhaba',)
(1923891389,)
(1923891389,)
(500,)
(5,)
(1923891389,)
(8394321923,)
```

Example 2:
```
print(sql.user_id_exists(1))
print(sql.user_telegram_id_exists(1923891389))
print(sql.user_id_exists(5))
print(sql.user_telegram_id_exists(1923891386))
```
Result:
```
Some bool (True in my case)
Some bool (True in my case)
Some bool (False in my case)
Some bool (False in my case)
```

Example 3
```
sql = Sql()
sql.make_new_user(63594,"some_referer",sql.REFER_USER).commit()
sql.make_new_user(17623,"some_customer",sql.CUSTOMER_USER).commit()
sql.make_new_referal(63594,17623).commit()
sql.get_all_referal_customers(63594).print_result()
```
