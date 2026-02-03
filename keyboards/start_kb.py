from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def start_keyboard():
    start_k = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='👀 О проекте', callback_data='info'),
                InlineKeyboardButton(text='Начать работу', callback_data='go_work')
            ]

        ]
            
           
    )
    return start_k

def back_to_start_keyboard():
    back_k = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Назад', callback_data='back_to_start')
        ]

    ]
    )

    return back_k

