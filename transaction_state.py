from aiogram.fsm.state import StatesGroup, State

class TransactionForm(StatesGroup):
    WAITING_FOR_AMOUNT = State()
    WAITING_FOR_DESCR = State()
    CONFIRM = State()
    CONTINUE = State()