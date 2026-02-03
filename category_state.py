from aiogram.fsm.state import StatesGroup, State

class AddCategoryState(StatesGroup):
    NAME_CATEGORY = State()
    TYPE_CATEGORY = State()