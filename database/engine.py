from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from database.models.base import BaseModel

DATABASE_URL = 'sqlite+aiosqlite:///./financebot.db'

engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(engine, expire_on_commit=False)

async def create_db():
    from database.models.user import User
    from database.models.category import Category
    from database.models.transactions import Transaction

    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)