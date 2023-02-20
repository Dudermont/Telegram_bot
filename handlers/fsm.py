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
