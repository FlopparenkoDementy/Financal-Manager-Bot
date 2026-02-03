import asyncio
from database.engine import create_db
from aiogram import Dispatcher, Bot
from handlers import register_routers
from middleware import register_middleware
from database import engine

BOT_API_TOKEN = '8508619668:AAHtAiP2Zka5uNBzMVApWrZOBXA1ZuKVlSE'
ADMINS_ID = [6466846793, 7864687059]

bot = Bot(BOT_API_TOKEN)
dp = Dispatcher()

async def main():
    await create_db()

    register_routers(dp)
    register_middleware(dp, engine.async_session)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот завершил работу')