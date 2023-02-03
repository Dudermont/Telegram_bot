import psycopg2
# from psycopg2 import Error
# from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from config import DB_CONECTION

conn = DB_CONECTION

cursor = conn.cursor()


def show_all():
    cursor.execute("SELECT * "
                   "FROM users;")
    res = cursor.fetchall()
    return res


def all_users():
    cursor.execute("SELECT * FROM users")
    res = cursor.fetchall()
    return res


def add_user(user, name):
    res = all_users()
    if len(res) == 0:
        cursor.execute("INSERT INTO users (user_name) VALUES (%s)", (user,))
        conn.commit()
        print("Пользователь добавлен в базу")
        return f'Добро пожаловать, {name}. \nВаша учетная запись зарегистрирована. \nНапишите /help или нажмите на команду, чтобы узнать, что может бот'
    for i in range(len(res)):
        if res[i][1] == user:
            print("Пользователь уже в базе")
            return f'Добро пожаловать,  { name}. \nНапишите /help или нажмите на команду, если нужна помощь.'
    cursor.execute("INSERT INTO users (user_name) VALUES (%s)", (user, ))
    conn.commit()
    print("Пользователь добавлен в базу")
    return f'Добро пожаловать, {name}. \nВаша учетная запись зарегистрирована. \nНапишите /help или нажмите на команду, чтобы узнать, что может бот'


def add_spend(category, operation_value, user):
    cursor.execute("INSERT INTO operation (user_id, category, operation_value) SELECT user_id, %s, %s FROM users "
                   "WHERE user_name = %s", (category, operation_value, user))
    conn.commit()
    print("Запись добавлена")
    return "Запись добавлена"


def all_spend(user):
    cursor.execute("SELECT SUM(operation_value) FROM operation INNER JOIN users USING(user_id) "
                   "WHERE user_name = %s", (user, ))
    conn.commit()
    res = cursor.fetchone()
    print("Вы потратили")
    return res


def category_spend(user, category):
    cursor.execute("SELECT SUM(operation_value) FROM operation INNER JOIN users USING(user_id) "
                   "WHERE user_name = %s  AND category = %s", (user, category))
    conn.commit()
    res = cursor.fetchone()
    print("Вы потратили")
    return res