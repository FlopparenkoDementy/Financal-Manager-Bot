from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters.callback_data import CallbackData


#class CategoryCBData(CallbackData, prefix='category'):#
#    category_id: int



#def generate_categ_kb(categories):
#    kb = InlineKeyboardMarkup(inline_keyboard=[])

#    for category in categories:#
#       kb.inline_keyboard.append(
#           [InlineKeyboardButton(text=category.name, 
#                                  callback_data=CategoryCBData(category_id=category.id).pack())]
#       )

#    kb.inline_keyboard.append(
#        [InlineKeyboardButton(text='➕ Добавить', callback_data='add_category')]
#    )

#    kb.inline_keyboard.append(
#        [InlineKeyboardButton(text='<< Назад', callback_data='go_work')]
#    )



# #   return kb


class CategoryCallback(CallbackData, prefix='cat'):
    id: int


def generate_categ_kb(user_categories: list):
    kb = InlineKeyboardMarkup(inline_keyboard=[])

    for cat in user_categories:
        kb.inline_keyboard.append(
            [InlineKeyboardButton(text=cat.name, 
                                  callback_data=CategoryCallback(id=cat.id).pack())]
        )

    kb.inline_keyboard.append(
        [InlineKeyboardButton(text='➕ Добавить', callback_data='add_category')]
    )

    kb.inline_keyboard.append(
        [InlineKeyboardButton(text='<< Назад', callback_data='go_work')]
    )

    return kb


def cancel_add(text: str = "Отменить"):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=text, callback_data='break_add')]
    ])

def is_expence_repl():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
            KeyboardButton(text='💰Доход')
            ],
            [
            KeyboardButton(text='💸Расход'),
            ]
        ],
        resize_keyboard=True
    )






def next_buttons():

    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text='Категории', callback_data='categories'),
        InlineKeyboardButton(text='Баланс', callback_data='balance'),
    ],
    [
        InlineKeyboardButton(text='Сформировать отчет', callback_data='make_ot')
    ]
    ])

    return kb