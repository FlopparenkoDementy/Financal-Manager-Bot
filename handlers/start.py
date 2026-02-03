from aiogram import Router
from aiogram import types, F
from aiogram.filters import Command
from aiogram.enums import ParseMode

from database.models.user import User
from repositoies.user import UserRepo
from keyboards.start_kb import start_keyboard, back_to_start_keyboard
from keyboards.work_k import next_buttons

router = Router()


@router.message(Command('start'))
async def start_bot(message: types.Message, user_repo: UserRepo):
    if await user_repo.is_in_base(message.from_user.id) == None:
        await user_repo.create_or_update_user(
            message.from_user.id,
            message.from_user.username,
            message.date
        )

        await message.answer(
            'Привет, я бот по контролю денежных средств\n\n'
            'Выбери что делать дальше из предложенных ниже вариантов',
            reply_markup=start_keyboard()
            )
    else:
        await user_repo.create_or_update_user(
            message.from_user.id,
            message.from_user.username,
            message.date
        )
        await message.answer(
            f'C возвращением {message.from_user.username}!',
            reply_markup=start_keyboard()
        )
    
@router.callback_query(F.data == 'back_to_start')
async def start_bot_again(callback: types.CallbackQuery):
    await callback.message.edit_text(
        'Выберите команду ниже для продолжения:',
        reply_markup=start_keyboard())
    

@router.callback_query(F.data == 'info')
async def show_info_about_project(callback: types.CallbackQuery):
    info_text = """
    <b>💰 Финансовый бот</b>

    Контролируйте доходы и расходы в Telegram

    <u>Основное:</u>
    • 📝 Учет операций с категориями
    • 📊 Статистика и графики
    • 🎯 Бюджет и лимиты
    • 📅 Фильтры по датам

    <u>Плюсы:</u>
    ⚡ Быстро | 📱 Удобно | 🔒 Безопасно
    <code>Используйте комаду /start чтобы начать</code>
    """
    await callback.message.edit_text(info_text,
    reply_markup=back_to_start_keyboard(), parse_mode='HTML'
    )

@router.callback_query(F.data == 'go_work')
async def start_work_bot(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Выберите что будем делать:", reply_markup=next_buttons())