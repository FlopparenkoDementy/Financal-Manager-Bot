from .start import router as start_router
from .category_handler import router as cate_router
from .transaction import router as transaction_router
from .broadcast import router as broadcast_router
from aiogram import Dispatcher


#Включение всех роутеров 
def register_routers(dp: Dispatcher):
    dp.include_router(broadcast_router)
    dp.include_router(start_router)
    dp.include_router(cate_router)
    dp.include_router(transaction_router)
