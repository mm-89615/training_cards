from sqlalchemy import select

from ..models import UserWord, User, Word
from .base import BaseRequest


class UserWordRequests(BaseRequest):
    async def get_all_user_words(self, tg_id: int):
        stmt = (select(Word)
                .join(User).where(User.tg_id == tg_id)
                .join(UserWord).where()
                .where(UserWord.user_id == User.id))
        result = await self.session.scalars(stmt)
        return result.all()