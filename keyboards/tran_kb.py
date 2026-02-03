from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from .work_k import CategoryCallback


class TransactionKeyboards:

    @property
    def cancel_kb(self):
        """Клавиатура отмены"""
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='❌ Отмена', callback_data='cancel_transaction')]
            ]
        )
    
    @property
    def skip_kb(self):
        """пропустить"""
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text='Пропустить')],
            ]
        )

    @property
    def confirmation_kb(self):
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='✅ Подтвердить', callback_data='confirm')],
                [InlineKeyboardButton(text="❌ Отменить", callback_data="cancel")]
            ]
        )
    
    @property
    def yes_or_no(self):
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='✅ Подтвердить', callback_data='do')],
                [InlineKeyboardButton(text="❌ Отменить", callback_data="dont")]
            ]
        )
    
    
    

def add_trans(category_id: int):
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='Добавить транзакцию', callback_data=CategoryCallback(id=category_id).pack())],
                [InlineKeyboardButton(text="« Назад к категориям", callback_data="categories")]
            ]
        )
    


transaction_kb = TransactionKeyboards()

def get_transaction_keyboards():
    return transaction_kb
