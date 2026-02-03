from aiogram import Bot, Router
from aiogram import types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states.broadcast_state import BroadcastState
from repositoies.user import UserRepo
from config import ADMINS_ID
import asyncio


router = Router()

@router.message(Command('broadcast'))
async def check_admin(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    if user_id not in ADMINS_ID:
        await message.answer('У вас нет прав администратора для данной попытки, обратитесь к администратору!')
        return False
    else:
        await message.answer('Введите сообщение для пользователей:')
        await state.set_state(BroadcastState.WAIT_FOR_MESSAGE)
        return True
    
@router.message(BroadcastState.WAIT_FOR_MESSAGE)
async def send_message_to_users(message: types.Message, 
                                state: FSMContext,
                                user_repo: UserRepo,
                                bot: Bot
                                ):
    
    users = await user_repo.get_len_user()

    broadcast_message = message.text

    await message.answer(f'Начинаем отправку сообщений для {len(users)}')

    success_cnt = 0
    fail_cnt = 0

    for user in users:
        try:
            await bot.send_message(chat_id=user,
                                   text=broadcast_message,
                                   parse_mode="HTML"
                                   )
            success_cnt += 1

            await asyncio.sleep(0.5)
        
        except Exception as e:
            fail_cnt += 1

    await state.clear()


    await message.answer(
    f"✅ Рассылка завершена!\n"
    f"Успешно: {success_cnt}\n"
    f"Не удалось: {fail_cnt}"
)



    