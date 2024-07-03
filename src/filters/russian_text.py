import re

from aiogram.filters import BaseFilter
from aiogram.types import Message


class RussianText(BaseFilter):
    pattern = re.compile(r"^[а-яА-Я0-9 ,.?()-]+$")

    async def __call__(self, message: Message) -> bool:
        return bool(self.pattern.match(message.text))
