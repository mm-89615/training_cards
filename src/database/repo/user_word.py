from typing import Optional

from sqlalchemy import select, func, update, delete
from sqlalchemy.dialects.postgresql import insert, INTERVAL
from sqlalchemy.sql.functions import concat

from .base import BaseRequest
from ..models import UserWord, Word


class UserWordRequests(BaseRequest):
    async def add_user_word(self, user_id: int, word_id: Optional[int], in_russian: str, in_english: str):
        if word_id:
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
        according Ebbinghaus's "The forgetting curve hypothesizes"
        1 repetition = 30 minutes
        2 repetition = 1 day
        3 repetition = 1 week
        4 repetition = 2 week
        5 and more repetitions = 2 month
        Priority for words with a lot of repetitions.
        """
        repetitions = UserWord.repetition_counter
        interval_30_min = UserWord.updated_at + func.cast(concat(30, "MINUTE"), INTERVAL) < func.now()
        interval_1_day = UserWord.updated_at + func.cast(concat(1, "DAY"), INTERVAL) < func.now()
        interval_1_week = UserWord.updated_at + func.cast(concat(1, "WEEK"), INTERVAL) < func.now()
        interval_2_week = UserWord.updated_at + func.cast(concat(2, "WEEK"), INTERVAL) < func.now()
        interval_2_month = UserWord.updated_at + func.cast(concat(2, "MONTH"), INTERVAL) < func.now()
        stmt = (select(UserWord)
                .where(UserWord.user_tg_id == tg_id)
                .where((repetitions == 0) |
                       ((repetitions == 1) & interval_30_min) |
                       ((repetitions == 2) & interval_1_day) |
                       ((repetitions == 3) & interval_1_week) |
                       ((repetitions == 4) & interval_2_week) |
                       ((repetitions >= 5) & interval_2_month))
                .order_by(UserWord.repetition_counter.desc(), UserWord.updated_at.asc())
                .limit(1))
        result = await self.session.scalars(stmt)
        return result.one_or_none()

    async def update_number_repetitions(self, word_id):
        stmt = (update(UserWord)
                .where(UserWord.id == word_id)
                .values(repetition_counter=UserWord.repetition_counter + 1))
        await self.session.execute(stmt)
        await self.session.commit()

    async def update_date(self, word_id):
        stmt = (update(UserWord)
                .where(UserWord.id == word_id)
                .values(updated_at=func.now()))
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_word_by_english(self, in_english: str, tg_id: int):
        stmt = (select(UserWord)
                .where(UserWord.in_english.ilike('%' + in_english + '%'))
                .where(UserWord.user_tg_id == tg_id))
        result = await self.session.scalars(stmt)
        return result.all()

    async def get_word_by_id(self, word_id: int, tg_id: int):
        stmt = (select(UserWord)
                .where(UserWord.id == word_id)
                .where(UserWord.user_tg_id == tg_id))
        result = await self.session.scalars(stmt)
        return result.one_or_none()

    async def delete_word(self, word_id: int, tg_id: int):
        stmt = (delete(UserWord)
                .where(UserWord.id == word_id)
                .where(UserWord.user_tg_id == tg_id))
        await self.session.execute(stmt)
        await self.session.commit()

    async def update_word(self, word_id: int, in_english: str, in_russian: str, tg_id: int):
        stmt = (update(UserWord)
                .where(UserWord.id == word_id)
                .where(UserWord.user_tg_id == tg_id)
                .values(in_english=in_english,
                        in_russian=in_russian))
        await self.session.execute(stmt)
        await self.session.commit()
