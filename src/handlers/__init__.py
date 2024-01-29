from aiogram import Dispatcher
from .start import router as start_routes


def register_routes(dp: Dispatcher):
    dp.include_router(start_routes)
