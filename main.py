from aiogram import Bot, Dispatcher, executor, types
from config import config
from lexicon import lexicon
import db_connect


bot = Bot(token=config.tg_bot.token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    res = db_connect.add_user(message.from_user.username, message.from_user.first_name)
    await message.answer(res)
    await message.delete()


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.answer(text=lexicon['help_menu'])
    await message.delete()
    print("Список команд")


@dp.message_handler(commands=['spending'])
async def start_number(message: types.Message):
    msg = message.text.split()
    category = msg[1].lower()
    operation_value = msg[2]
    if operation_value.find(',') != -1:
        operation_value = operation_value.replace(',', '.')
    print(operation_value)
    res = db_connect.add_spend(category, operation_value, message.from_user.username)
    await message.answer(res)


@dp.message_handler(commands=['expense'])
async def start_number(message: types.Message):
    res = db_connect.all_spend(message.from_user.username)
    await message.answer("Вы потратили:")
    await message.answer(*res)


@dp.message_handler(commands=['category'])
async def start_number(message: types.Message):
    msg = message.text.split()
    category = msg[1].lower()
    res = db_connect.category_spend(message.from_user.username, category)
    await message.answer(f"Вы потратили на {category}:")
    await message.answer(*res)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
