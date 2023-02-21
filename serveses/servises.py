from database.db_connect import add_spend, category_spend, day_spend, month_spend, year_spend, period_spend
from keyboards.keyboard import month4


def val_category_spend(tupl: tuple) -> float:
    if tupl[0] is None:
        return 0
    else:
        return tupl[0]


def send_spend_dp(user_data: dict[str, str]):
    category = user_data['category'].lower()
    operation_value = user_data['cash']
    if operation_value.find(',') != -1:
        operation_value = operation_value.replace(',', '.')
    username = user_data['username']
    res = add_spend(category, operation_value, username)
    return res


def spend_category(user_data: dict[str, str]):
    username = user_data['username']
    category = user_data['category'].lower()
    res = category_spend(username, category)
    return val_category_spend(res)


def day_db_select(user_date: dict[str, str]) -> tuple:
    return day_spend(user_date['date'], user_date['username'])


def month_db_select(user_date: dict[str, str]):
    if user_date['month'] in month4:
        user_date['month'] = month4[user_date['month']]
    res = month_spend(user_date['month'], user_date['year'], user_date['username'])
    if user_date['month'] in month4.values():
        d = {value: key for key, value in month4.items()}
        user_date['month'] = d[user_date['month']]
    if res[0] is None:
        return 0
    else:
        return res[0]


def year_db_select(user_date: dict[str, str]):
    res = year_spend(user_date['year'], user_date['username'])
    if res[0] is None:
        return 0
    else:
        return res[0]


def period_db_select(user_date: dict[str, str]):
    res = period_spend(user_date['first_year'], user_date['second_year'], user_date['username'])
    if res[0] is None:
        return 0
    else:
        return res[0]
