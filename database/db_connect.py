import psycopg2
# from psycopg2 import Error
# from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from config.config import config
from lexicon.lexicon import lexicon
from database.database_select import select

conn = psycopg2.connect(dbname=config.db.dbname,
                        user=config.db.user,
                        password=config.db.password,
                        host=config.db.host)

cursor = conn.cursor()


def show_all():
    cursor.execute(select['show_all'])
    res = cursor.fetchall()
    return res


def _all_users():
    cursor.execute(select['all_users'])
    res = cursor.fetchall()
    return res


def add_user(user, name):
    res = _all_users()
    if len(res) == 0:
        cursor.execute(select['add_user'], (user,))
        conn.commit()
        print("Пользователь добавлен в базу")
        return f'Добро пожаловать, {name}.' + lexicon['registration']
    for i in range(len(res)):
        if res[i][1] == user:
            print("Пользователь уже в базе")
            return f'Добро пожаловать,  { name}. \nНапишите /help или нажмите на команду, если нужна помощь.'
    cursor.execute(select['add_user'], (user, ))
    conn.commit()
    print("Пользователь добавлен в базу")
    return f'Добро пожаловать, {name}.' + lexicon['registration']


def add_spend(category, operation_value, user):
    cursor.execute(select['add_spend'], (category, operation_value, user))
    conn.commit()
    print("Запись добавлена")
    return "Запись добавлена ✅"


def all_spend(user):
    cursor.execute(select['all_spend'], (user, ))
    conn.commit()
    res = cursor.fetchone()
    print("Вы потратили")
    return res


def category_spend(user, category):
    cursor.execute(select['category_spend'], (user, category))
    res = cursor.fetchone()
    print("Вы потратили")
    return res


def day_spend(date, username):
    cursor.execute(select['day_spend'], (date, username))
    res = cursor.fetchone()
    print(f"Потратили за {date}")
    return res


def month_spend(month, year, username):
    cursor.execute(select['month_spend'], (month, year, username))
    res = cursor.fetchone()
    print(f"Потратили за {month}")
    return res


def year_spend(year, username):
    cursor.execute(select['year_spend'], (year, username))
    res = cursor.fetchone()
    print(f"Потратили за {year}")
    return res


def period_spend(first_year, second_year, username):
    cursor.execute(select['period_spend'], (first_year, second_year, username))
    res = cursor.fetchone()
    print(f"Потратили с {first_year} по {second_year}:")
    return res