from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import Message

from repositoies.user import UserRepo
from repositoies.category import CategoryRepo
from repositoies.transaction import TransationRepo

#Класс для автоматической сессии подключения к базе данных
class DatabaseSessionMiddleware(BaseMiddleware):
    def __init__(self, session_maker) -> None:
        self.session_maker = session_maker



    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], 
                       event: Message, 
                       data: Dict[str, Any]):
        async with self.session_maker() as session:
            data['user_repo'] = UserRepo(session=session)
            data['category_repo'] = CategoryRepo(session=session)
            data['tran_repo'] = TransationRepo(session=session)
            return await handler(event, data)
        
        