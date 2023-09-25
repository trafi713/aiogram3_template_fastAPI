from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsPrivateFilter(BaseFilter):
    async def __call__(self, obj: Message):
        return obj.chat.type == 'private'

