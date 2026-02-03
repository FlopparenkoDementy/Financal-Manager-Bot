from aiogram.fsm.state import StatesGroup, State

class BroadcastState(StatesGroup):
    WAIT_FOR_MESSAGE = State()