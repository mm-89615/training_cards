import re

from aiogram.filters import BaseFilter
from aiogram.types import Message


class EnglishText(BaseFilter):
    pattern = re.compile(r"^[a-zA-Z0-9 ',.?()-]+$")

    async def __call__(self, message: Message) -> bool:
        return bool(self.pattern.match(message.text))
