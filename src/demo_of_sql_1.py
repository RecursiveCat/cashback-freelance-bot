import sql

#РАБОТАЕМ С КЛАССОМ SQL
sql = sql.Sql()

#Запишем айди для удобства
zhaba_id = 777777777
cat_id = 88888

#Как проверить, существует ли юзер
if sql.user_exists(zhaba_id):
    print(f"User {sql.get_user_name_by_id(zhaba_id)} - exists!")
if sql.user_exists(cat_id):
    print(f"User {sql.get_user_name_by_id(cat_id)} - exists!")


#Создадим нового юзера
test_user1 = {
    "id" : 999999999, #желательно только 9 символов
    "name": "TESTUSER1", 
    "type": "admin" # admin,customer,operator
}

sql.create_user_as(
    test_user1["id"],
    test_user1["name"],
    test_user1["type"]
)
if sql.user_exists(cat_id):
    print(f"User {sql.get_user_name_by_id(test_user1['id'])} - exists!")

#Создадим организацию с админом в качестве test_user1
gazprom = {
    "name":"OAO GAZPROM",
    "id":99999,
    "admin":test_user1["id"],
}

#!!! СОЗДАВАТЬ ТОЛЬКО ПОСЛЕ ПРОВЕРКИ ИБО ЭТА БАНДУРА СОЗДАЕТ ОДИНАКОВЫЕ ЗАПИСИ#
# исправлю позже
if not sql.institution_exists(99999):   
    sql.make_institution(gazprom["id"],gazprom["name"],gazprom["admin"])
print(sql.is_admin(gazprom["admin"]))

#chmod 777
sql.change_permissions_by_uid(gazprom["admin"],{
    "admin":"TRUE",
    "operator":"TRUE",   #как супер пользователь в линуксе, везде 777
    "customer":"TRUE",   
})


sql.change_user_bonuses(zhaba_id,777,77777)

#создаем операцию
op1 = {
    "bonuses":999,
    "user":{
        "id":999999999
    },
    "institution":{
        "id":gazprom["id"]
    }
}

sql.create_operation_node_by_adding_bonuses(
    op1["user"]["id"],
    op1["bonuses"],
    op1["institution"]["id"]   
)

print(sql.get_all_bonuses_stuff(op1["user"]["id"]))
