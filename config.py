from dataclasses import dataclass
from environs import Env


HELP_COMMAND = """
/start - Приветствие
/help - Список команд
/spending - Внести траты в формате: /spending категория_трат сумма \n(НАПРИМЕР: /spending цветы 570.99)
/expense - Выводит сколько вы потратили
/category - Выводит сколько вы потратили по категориям \n(НАПРИМЕР: /category цветы)
"""


@dataclass
class DatabaseConfig:
    dbname: str
    user: str
    password: str
    host: str


@dataclass
class TgBot:
    token: str


@dataclass
class Config:
    tg_bot: TgBot
    db: DatabaseConfig


env: Env = Env()
env.read_env()
config = Config(
                tg_bot=TgBot(
                              token=env("API_TOKEN")
                            ),
                db=DatabaseConfig(
                                  dbname=env("dbname"),
                                  user=env("user"),
                                  password=env("password"),
                                  host=env("host")
                                  )
                )
