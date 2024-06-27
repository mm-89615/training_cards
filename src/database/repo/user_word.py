from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import insert

from .base import BaseRequest
from ..models import UserWord


class UserWordRequests(BaseRequest):
    async def add_user_word(self, user_id: int, word_id: Optional[int], in_russian: str, in_english: str):
        if word_id:
            stmt = (insert(UserWord)
                    .values(user_id=user_id,
                            word_id=word_id,
                            in_russian=in_russian,
                            in_english=in_english))
        else:
            stmt = (insert(UserWord)
                    .values(user_id=user_id,
                            in_russian=in_russian,
                            in_english=in_english))
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_new_word_from_user_words(self, tg_id: int):
        """
        Get random word from user words
        """
        stmt = (select(UserWord)
                .where(UserWord.user_tg_id == tg_id)
                .order_by(func.random())
                .limit(1))
        result = await self.session.scalars(stmt)
        return result.one_or_none()
