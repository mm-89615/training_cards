from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from .user import UserRequests
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
