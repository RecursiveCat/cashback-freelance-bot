# Cashback by bonuses bot

Телеграм бот,который будет учитывать накопленные бонусы при совершении покупок. 

Существует 3 типа пользователей:<br>
Продавец, Оператор, Покупатель<br>
<br>
Продавец умеет:<br> 
  1. Задавать процент бонусов 
  2. Задавать процент реферальных вознаграждений
  3. Начислять бонусы клиентам
  4. Списать бонусы у клиентов

Оператор:
  pass

Покупатель умеет:
  1. Сообщать код продавцу
  2. Списывать бонусы
  3. Получить реферальную ссылку

каждый тип имеет свои кнопки и функции

Покупатель коммуницирует с оператором, чтобы совершить покупку, 
используя бонусы. Пользователь получает дополнительный процент 
ко всем покупкам, если он приглашает другого потенциального 
пользователя используя реферальную ссылку, 
кликнув на которую приглашенный закрепляется к пригласителю.
Пользователь может получить бонусы, если продавец нажимает на кнопку 
"Начислить бонусы", он выбирает, кому начислить бонусы и этому 
пользователю в личку приходит ссылка, нажав на которую пользователю 
начисляются бонусы. Так же у пользователя могут снять бонусы, 
для этого продавец используя кнопку "списать бонусы" выбирает 
пользователя и спрашивает у него суммы покупки (не знаю зачем) и 
код операции, оператор вводит этот код в бот и после бот удаляет 
эти бонусы по этому коду. по кнопке "бонусы" - человек связывается
с оператором и говорит о своей операции. по кнопке "мои бонусы" 
пользователь может посмотреть коды операций и бонус


Структура БД:
Пользователи:
 идентификатор пользователя INT
 тип пользователя STR
 к кому привязан (идентификатор пригласившего) INT
 Бонусы INT
 Проценты INT

Операции:
 Номер операции INT
 Сумма покупки BIGINT
 Бонусы INT

Главная задача жабы: прописать SQL класс, чтобы можно было взаимодействовать с MySQL, функции буду просить в процессе.

Главная задача кота: обвернуть в телеграм бота, прописать кнопки и базовые функции
```
Class Sql:

    var data_base_connection
    var data_base_cursor
    var last_query

    def __init__(self)
    def run(self,query)
    def select(self,data,table,condition=None)
    def commit(self)
    def get_user_type_by_id(self,id)
    def get_user_all_bonuses_by_id(self,id)
    def get_user_percent_from_price_by_id(self,id)
    def get_user_name_by_id(self,id)
    def get_user_tg_id_by_id(self,id)
    def get_referal_id_by_id(self,id)
    def get_operation_price_by_id(self,id)
    def get_operation_bonuses_by_id(self,id)
    def get_operation_money_to_user_telegram_id_by_id(self,id)
    def get_operation_bonuses_to_user_telegram_id_by_id(self,id)
    def print_result(self)
```

Examlpe 1 :

```
sql = Sql()
sql.run("SHOW TABLES")
sql.print_result()
sql.select("*","users")
sql.print_result()
sql.get_user_type_by_id(1)
sql.print_result()def get_referal_id_by_id(self,id)

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
