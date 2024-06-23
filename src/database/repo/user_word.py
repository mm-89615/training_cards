from sqlalchemy import select

from ..models import UserWord
from .base import BaseRequest


class UserWordRequests(BaseRequest):
    async def get_all_user_words(self, user_id: int):
        stmt = select(UserWord).where(UserWord.user_id == user_id)
        result = await self.session.scalars(stmt)
        return result.all()