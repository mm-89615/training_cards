from aiogram.filters import BaseFilter
from aiogram.types import Message

from config import settings


class IsAdmin(BaseFilter):
    def __init__(self):
        self.users_ids = settings.bot.admin_ids

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.users_ids
