from typing import Optional

from sqlalchemy import select, func, update
from sqlalchemy.dialects.postgresql import insert

from .base import BaseRequest
from ..models import UserWord, Word


class UserWordRequests(BaseRequest):
    async def add_user_word(self, user_id: int, word_id: Optional[int], in_russian: str, in_english: str):
        if word_id:
            # word = select(Word).where(Word.id == word_id)
            word = await self.session.scalars(select(Word).where(Word.id == word_id))
            word = word.one_or_none()
            stmt = (insert(UserWord)
                    .values(user_tg_id=user_id,
                            word_id=word_id,
                            in_russian=word.in_russian,
                            in_english=word.in_english))
        else:
            stmt = (insert(UserWord)
                    .values(user_tg_id=user_id,
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

    async def update_number_repetitions(self, word_id):
        stmt = (update(UserWord)
                .where(UserWord.id == word_id)
                .values(repetition_counter=UserWord.repetition_counter + 1))
        await self.session.execute(stmt)
        await self.session.commit()