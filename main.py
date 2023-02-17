from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import Message
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import config
from lexicon import lexicon
from keyboard import keyboard_1, keyboard_2
import db_connect

storage: MemoryStorage = MemoryStorage()
bot = Bot(token=config.tg_bot.token)
dp = Dispatcher(bot, storage=storage)


class FSMFillspending(StatesGroup):
    fill_spend = State()
    fill_category = State()


class FSMCategoryspend(StatesGroup):
    fill_category = State()


def send_spend_dp(user_data: dict[str, str]):
    category = user_data['category'].lower()
    operation_value = user_data['cash']
    if operation_value.find(',') != -1:
        operation_value = operation_value.replace(',', '.')
    username = user_data['username']
    res = db_connect.add_spend(category, operation_value, username)
    return res


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    res = db_connect.add_user(message.from_user.username, message.from_user.first_name)
    await message.answer(res, reply_markup=keyboard_2)
    await message.delete()


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.answer(text=lexicon['help_menu'], reply_markup=keyboard_1)
    await message.delete()
    print("Список команд")


def expense(username):
    return db_connect.all_spend(username)


def spend_category(user_data: dict[str, str]):
    username = user_data['username']
    category = user_data['category'].lower()
    res = db_connect.category_spend(username, category)
    return res


@dp.callback_query_handler(text='help')
async def inline_kb_answer_help(query: types.CallbackQuery):
    await help_command(query.message)


@dp.callback_query_handler(text='spending')
async def inline_kb_answer_spending(query: types.CallbackQuery):
    await query.message.answer(text='Введите сумму')
    await FSMFillspending.fill_spend.set()


@dp.message_handler(state=FSMFillspending.fill_spend)
async def take_spend(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['cash'] = message.text
    await message.answer(text='Спасибо, а теперь введите категорию')
    await FSMFillspending.fill_category.set()


@dp.message_handler(state=FSMFillspending.fill_category)
async def take_spend(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['username'] = message.from_user.username
        data['category'] = message.text
    user_spend = await state.get_data()
    await message.answer(send_spend_dp(user_spend))
    await message.answer(text='Пока не придумал чего написать', reply_markup=keyboard_2)
    await state.reset_state()
    print(user_spend)


@dp.callback_query_handler(text='expense')
async def inline_kb_answer_category(query: types.CallbackQuery):
    await query.message.answer("Вы потратили:")
    await query.message.answer(*expense(query.message.chat.username))


@dp.callback_query_handler(text='category')
async def inline_kb_answer_category(query: types.CallbackQuery):
    await query.message.answer(text='Введите категорию')
    await FSMCategoryspend.fill_category.set()


@dp.message_handler(state=FSMCategoryspend.fill_category)
async def give_expense(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['username'] = message.from_user.username
        data['category'] = message.text
    user_spend = await state.get_data()
    await message.answer(f"Вы потратили на {data['category']}:")
    await message.answer(*spend_category(user_spend))
    await message.answer(text='Пока не придумал чего написать', reply_markup=keyboard_2)
    await state.reset_state()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
