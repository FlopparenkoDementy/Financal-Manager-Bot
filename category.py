from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.category import Category



class CategoryRepo:
    def __init__(self, session: AsyncSession):
        self.__session = session
 
    async def get_list_by_user_id(self, user_id: int):
        statement = (
            select(Category).where(Category.user_id == user_id).order_by(Category.name)
        )
        result = await self.__session.scalars(statement)
        return result.all()
    
    async def add_new_category(self, name: str, user_id: int, is_expense: bool):
        try:
            category = Category(
                name=name,
                user_id=user_id,
                is_expense=is_expense  # Может быть None
            )
            
            self.__session.add(category)
            await self.__session.commit()
            return category
        except Exception:
            await self.__session.rollback()
            raise

    async def get_is_expense(self, user_id: int):
        statement = select(Category.is_expense).where(Category.user_id == user_id)
        result = await self.__session.execute(statement)
        return result.scalar()
    
    async def get_category_name(self, category_id: int):
        statement = select(Category.name).where(Category.id == category_id)
        result = await self.__session.execute(statement)
        return result.scalar()
    
    
        
