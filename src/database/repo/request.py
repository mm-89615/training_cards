from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from .user import UserRequests
from .user_word import UserWordRequests
from .word import WordRequests


@dataclass
class Request:
    session: AsyncSession

    @property
    def users(self) -> UserRequests:
        return UserRequests(self.session)

    @property
    def words(self) -> WordRequests:
        return WordRequests(self.session)

    @property
    def user_words(self) -> UserWordRequests:
        return UserWordRequests(self.session)
