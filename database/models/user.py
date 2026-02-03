from sqlalchemy.orm import mapped_column, Mapped 
from datetime import date
from sqlalchemy import BigInteger 
from .base import BaseModel


class User(BaseModel):

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    username: Mapped[str | None]

    created_at: Mapped[date] = mapped_column(default=date.today)
    