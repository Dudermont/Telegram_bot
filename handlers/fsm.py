from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup


storage: MemoryStorage = MemoryStorage()


class FSMFillspending(StatesGroup):
    fill_spend = State()
    fill_category = State()


class FSMCategoryspend(StatesGroup):
    fill_category = State()


class FSMDuringDay(StatesGroup):
    fill_date = State()


class FSMDuringMonth(StatesGroup):
    fill_month = State()


class FSMDuringYear(StatesGroup):
    fill_year = State()


class FSMDuringDuring(StatesGroup):
    fill_first_date = State()
    fill_second_date = State()
