from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import ForeignKey, String
from datetime import date
from .base import BaseModel

class Transaction(BaseModel):

    __tablename__ = 'transactions'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    description: Mapped[str] = mapped_column(String)
    amount: Mapped[int] = mapped_column(nullable=False)
    created: Mapped[date] = mapped_column(default=date.today)
