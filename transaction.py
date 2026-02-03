from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from database.models.transactions import Transaction
from datetime import datetime

class TransationRepo:

    def __init__(self, session: AsyncSession):
        self.__session = session


    async def check_category_has_transaction(self, category_id: int):
        statement = select(Transaction).where(Transaction.category_id == category_id)
        result = await self.__session.execute(statement)
        transaction = result.first()

        return transaction 
    

    async def get_transactions_by_category_id(self, category_id: int):
        statement = select(Transaction).where(Transaction.category_id == category_id).order_by(Transaction.created.desc())
        result = await self.__session.execute(statement)
        return result.scalars().all()
    
    async def save_transaction_to_db(self, data: dict, user_id):
        transaction = Transaction(
            user_id=user_id,
            category_id=data['category_id'],
            description=data['descr'],
            amount=data['amount'],
            created=datetime.now()
        )

        self.__session.add(transaction)

        await self.__session.commit()

        return transaction
    
    
    