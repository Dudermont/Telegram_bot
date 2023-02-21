from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from keyboards.keyboard import keyboard_1, keyboard_2
from lexicon.lexicon import lexicon
from database.db_connect import add_user


# Реагирует на команду /help
async def help_command(message: types.Message):
    await message.answer(text=lexicon['help_menu'], reply_markup=keyboard_1)
    await message.delete()
    print("Список команд")


# Реагирует на команду /start
async def start_command(message: types.Message):
    res = add_user(message.from_user.username, message.from_user.first_name)
    await message.answer(res, reply_markup=keyboard_2)
    await message.delete()


# Реагирует на команду /cancel
# async def cansel_command(message: types.Message, state: FSMContext):
#     await message.answer(lexicon['cancel'])
#     await state.reset_state()


# Регистрация команд
def registration_command_handler(dp: Dispatcher):
    dp.register_message_handler(help_command, commands='help')
    dp.register_message_handler(start_command, commands='start')
    # dp.register_message_handler(cansel_command, commands='cancel')
