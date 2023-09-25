from aiogram import types, Router
from aiogram.filters import Command

from src.filters.is_private import IsPrivateFilter

start_router = Router()
start_router.message.filter(IsPrivateFilter())


@start_router.message(Command('start'))
async def start_handler(message: types.Message):
    await message.answer(f"Hey {message.from_user.first_name}")
