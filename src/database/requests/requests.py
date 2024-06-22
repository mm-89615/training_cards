from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from .user import UserRequests


@dataclass
class Requests:
    session: AsyncSession

    @property
    def users(self) -> UserRequests:
        return UserRequests(self.session)
