from datetime import date
from aiogram import Dispatcher
from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher import FSMContext
from database import db_connect
from handlers.commands import help_command
from handlers.fsm import FSMFillspending, FSMCategoryspend, FSMDuringDay, FSMDuringMonth, FSMDuringYear, FSMDuringDuring
from keyboards.keyboard import keyboard_2, spend_during_keyboard, cancel_keyboard, month3
from serveses.servises import (send_spend_dp, spend_category, day_db_select,
                               month_db_select, year_db_select, period_db_select)
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


async def wrong_take_cash(massage: Message):
    await massage.answer(lexicon['cash_error'])


async def take_cash(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['cash'] = message.text
    await message.answer(text='Спасибо, а теперь введите категорию', reply_markup=cancel_keyboard)
    await FSMFillspending.fill_category.set()


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


# Ответ на кнопку month
async def inline_kb_answer_month(query: CallbackQuery):
    await query.message.delete()
    await query.message.answer('Введите месяц', reply_markup=cancel_keyboard)
    await FSMDuringMonth.fill_month.set()


async def wrong_expense_per_month(message: Message):
    await message.answer(lexicon['month_error'])


async def give_expense_per_month(message: Message, state: FSMContext):
    await message.delete()
    async with state.proxy() as data:
        data['month'] = message.text.title()
        data['year'] = date.today().year
        data['username'] = message.chat.username
    user_date = await state.get_data()
    print(user_date)
    await message.answer(f'Вы потратили за {user_date["month"]}')
    await message.answer(month_db_select(user_date))
    await state.reset_state()


# Ответ на кнопку year
async def inline_kb_answer_year(query: CallbackQuery):
    await query.message.delete()
    await query.message.answer('Введите год', reply_markup=cancel_keyboard)
    await FSMDuringYear.fill_year.set()


async def wrong_expense_per_year(message: Message):
    await message.answer(lexicon['year_error'])


async def give_expense_per_year(message: Message, state: FSMContext):
    await message.delete()
    async with state.proxy() as data:
        data['year'] = message.text
        data['username'] = message.chat.username
    user_date = await state.get_data()
    print(user_date)
    await message.answer(f'Вы потратили за {user_date["year"]} год')
    await message.answer(year_db_select(user_date))
    await state.reset_state()


# Ответ на кнопку period
async def inline_kb_answer_period(query: CallbackQuery):
    await query.message.delete()
    await query.message.answer('Введите первую дату гггг-мм-дд', reply_markup=cancel_keyboard)
    await FSMDuringDuring.fill_first_date.set()


async def take_first_date(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['first_year'] = message.text
    await message.answer(text='Спасибо, а теперь вторую гггг-мм-дд', reply_markup=cancel_keyboard)
    await FSMDuringDuring.fill_second_date.set()


async def give_expense_period(message: Message, state: FSMContext):
    await message.delete()
    async with state.proxy() as data:
        data['second_year'] = message.text
        data['username'] = message.chat.username
    user_date = await state.get_data()
    print(user_date)
    await message.answer(f'Вы потратили c {user_date["first_year"]} по {data["second_year"]}:')
    await message.answer(period_db_select(user_date))
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
                                lambda x: x.text.isdigit() and len(
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
    dp.register_callback_query_handler(inline_kb_answer_month, text='month')
    dp.register_message_handler(give_expense_per_month,
                                lambda x: (x.text.isdigit() and 1 <= int(x.text) <= 12) or len(
                                    x.text.split()) == 1 and x.text.title() in month3.values(),
                                state=FSMDuringMonth.fill_month)
    dp.register_message_handler(wrong_expense_per_month, content_types='any', state=FSMDuringMonth.fill_month)
    dp.register_callback_query_handler(inline_kb_answer_year, text='year')
    dp.register_message_handler(give_expense_per_year,
                                lambda x: x.text.isdigit() and 1 <= int(x.text) <= 9999,
                                state=FSMDuringYear.fill_year)
    dp.register_message_handler(wrong_expense_per_year, content_types='any', state=FSMDuringYear.fill_year)
    dp.register_callback_query_handler(inline_kb_answer_period, text='period')
    dp.register_message_handler(take_first_date, state=FSMDuringDuring.fill_first_date)
    dp.register_message_handler(give_expense_period, state=FSMDuringDuring.fill_second_date)
    dp.register_callback_query_handler(inline_kb_cancel, state='*')
