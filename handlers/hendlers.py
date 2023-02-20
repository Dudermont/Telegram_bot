from aiogram import Dispatcher
from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher import FSMContext
from database import db_connect
from handlers.commands import help_command
from handlers.fsm import FSMFillspending, FSMCategoryspend, FSMDuringDay
from keyboards.keyboard import keyboard_2, spend_during_keyboard, cancel_keyboard
from serveses.servises import send_spend_dp, spend_category, day_db_select
from lexicon.lexicon import lexicon


# ответ на кнопку help
async def inline_kb_answer_help(query: CallbackQuery):
    await help_command(query.message)


# Ответ на кнопку expense
async def inline_kb_answer_expense(query: CallbackQuery):
    await query.message.delete()
    await query.message.answer("Вы потратили:")
    await query.message.answer(*db_connect.all_spend(query.message.chat.username))


# Ответ на кнопку spending
async def inline_kb_answer_spending(query: CallbackQuery):
    await query.message.delete()
    await query.message.answer(text='Введите сумму', reply_markup=cancel_keyboard)
    await FSMFillspending.fill_spend.set()


async def take_cash(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['cash'] = message.text
    await message.answer(text='Спасибо, а теперь введите категорию', reply_markup=cancel_keyboard)
    await FSMFillspending.fill_category.set()


async def wrong_take_cash(massage: Message):
    await massage.answer(lexicon['cash_error'])


async def take_category(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['username'] = message.from_user.username
        data['category'] = message.text
    user_spend = await state.get_data()
    await message.answer(send_spend_dp(user_spend))
    await message.answer(text='Пока не придумал чего написать', reply_markup=keyboard_2)
    await state.reset_state()
    print(user_spend)


# Ответ на кнопку category
async def inline_kb_answer_category(query: CallbackQuery):
    await query.message.delete()
    await query.message.answer(text='Введите категорию', reply_markup=cancel_keyboard)
    await FSMCategoryspend.fill_category.set()


async def give_expense(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['username'] = message.from_user.username
        data['category'] = message.text
    user_spend = await state.get_data()
    await message.answer(f"Вы потратили на {data['category']}:")
    await message.answer(spend_category(user_spend))
    await message.answer(text='Пока не придумал чего написать', reply_markup=keyboard_2)
    await state.reset_state()


# Ответ на кнопку during
async def inline_kb_answer_during(query: CallbackQuery):
    await query.message.answer("Бурлык", reply_markup=spend_during_keyboard)
    await query.message.delete()


# Ответ на кнопку day
async def inline_kb_answer_day(query: CallbackQuery):
    await query.message.answer("Введите дату гггг-мм-дд", reply_markup=cancel_keyboard)
    await FSMDuringDay.fill_date.set()


async def give_expense_per_day(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['username'] = message.from_user.username
        data['date'] = message.text
    user_date = await state.get_data()
    print(user_date)
    await message.answer(f"Вы потратили за {data['date']}:")
    await message.answer(*day_db_select(user_date))
    await message.answer(text='Пока не придумал чего написать', reply_markup=keyboard_2)
    await state.reset_state()


# Ответ на кнопку canсel
async def inline_kb_cancel(query: CallbackQuery, state: FSMContext):
    await query.message.delete()
    await query.message.answer(lexicon['cancel'])
    await state.reset_state()


# Регистрация хэндлеров
def registration_handler(dp: Dispatcher):
    dp.register_callback_query_handler(inline_kb_answer_expense, text='expense')
    dp.register_callback_query_handler(inline_kb_answer_help, text='help')
    dp.register_callback_query_handler(inline_kb_answer_spending, text='spending')
    dp.register_message_handler(take_cash,
                                lambda x: len(
                                    str(
                                        float(x.text)
                                    ).split('.')[0]
                                ) <= 8 and len(
                                    str(
                                        float(x.text)
                                    ).split('.')[1]
                                ) <= 2 and int(x.text) >= 0,
                                state=FSMFillspending.fill_spend)
    dp.register_message_handler(wrong_take_cash, content_types='any', state=FSMFillspending.fill_spend)
    dp.register_message_handler(take_category, state=FSMFillspending.fill_category)
    dp.register_callback_query_handler(inline_kb_answer_category, text='category')
    dp.register_message_handler(give_expense, state=FSMCategoryspend.fill_category)
    dp.register_callback_query_handler(inline_kb_answer_during, text='during')
    dp.register_callback_query_handler(inline_kb_answer_day, text='day')
    dp.register_message_handler(give_expense_per_day, state=FSMDuringDay.fill_date)
    dp.register_callback_query_handler(inline_kb_cancel, state='*')
