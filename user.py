from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from database.models.user import User
from datetime import date


"""Класс UserRepo (user repository), создан для обращения к базе данных и 
исходя из данных формировать отчеты итп. также создания методов работы"""


class UserRepo:
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def is_in_base(self, tg_id: int):
        user = await self.get_user_by_tg_id(tg_id)
        if not user:
            return None
        else:
            return True


    async def get_user_by_tg_id(self, tg_id: int):
        statement = select(User).where(User.tg_id == tg_id)
        return await self.__session.scalar(statement)

    async def create_user(self, tg_id: int, username: str | None, created_at: date):
        user = User(tg_id=tg_id, username=username, created_at=created_at)
        self.__session.add(user)
        await self.__session.commit()
        await self.__session.refresh(user)
        return user
    
    async def create_or_update_user(self, tg_id: int, username: str, created_at: date):
        user = await self.get_user_by_tg_id(tg_id=tg_id)

        if not user:
            user = await self.create_user(tg_id, username, created_at)
        else:
            user.username = username
            await self.__session.commit()
            await self.__session.refresh(user)

        return user
    
    async def get_len_user(self):
        statement = select(User.tg_id)
        result = await self.__session.execute(statement)
        return result.scalars().all()
