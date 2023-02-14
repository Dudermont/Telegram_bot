from dataclasses import dataclass
from environs import Env


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
