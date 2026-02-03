from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import ForeignKey
from .base import BaseModel

class Category(BaseModel):

    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    is_expense: Mapped[bool]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
