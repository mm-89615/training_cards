from typing import Optional

from sqlalchemy import select, func, union_all, delete, update
from sqlalchemy.dialects.postgresql import insert

from .base import BaseRequest
from ..models import Word, UserWord


class WordRequests(BaseRequest):
    async def add_word(self, in_english: str, in_russian: str):
        stmt = (insert(Word)
                .values(in_english=in_english,
                        in_russian=in_russian))
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_new_word_not_in_user_words(self, tg_id: int, old_word_id: Optional[int] = None):
        """
        Get new word from common words where word not in user words
        """
        stmt = (select(Word)
                .where(Word.id.not_in((select(UserWord.word_id)
                                       .where(UserWord.user_tg_id == tg_id,
                                              UserWord.word_id.is_not(None)))))
                .order_by(func.random())
                .limit(1))
        result = await self.session.scalars(stmt)
        return result.one_or_none()

    async def get_three_random_words(self, word_id: int):
        """
        Get 3 random words from common words
        excluding the word that was extracted for study
        """
        stmt = (select(Word)
                .where(Word.id.not_in([word_id]))
                .order_by(func.random())
                .limit(3))
        result = await self.session.scalars(stmt)
        return result.all()

    async def get_four_random_words(self, tg_id: int):
        """
        Get 4 random words from common or user words
        """
        stmt1 = select(Word.id, Word.in_english, Word.in_russian)
        stmt2 = (select(UserWord.word_id, UserWord.in_english, UserWord.in_russian)
                 .where(UserWord.word_id.is_(None), UserWord.user_tg_id == tg_id))
        union_stmt = (select(union_all(stmt1, stmt2).subquery())
                      .order_by(func.random())
                      .limit(4))
        result = await self.session.execute(union_stmt)
        return result.all()

    async def get_word_by_english(self, in_english: str):
        stmt = (select(Word)
                .where(Word.in_english.ilike('%' + in_english + '%')))
        result = await self.session.scalars(stmt)
        return result.all()

    async def get_word_by_id(self, word_id: int):
        stmt = (select(Word)
                .where(Word.id == word_id))
        result = await self.session.scalars(stmt)
        return result.one_or_none()

    async def delete_word(self, word_id: int):
        stmt = (delete(Word)
                .where(Word.id == word_id))
        await self.session.execute(stmt)
        await self.session.commit()

    async def update_word(self, word_id: int, in_english: str, in_russian: str):
        stmt = (update(Word)
                .where(Word.id == word_id)
                .values(in_english=in_english,
                        in_russian=in_russian))
        await self.session.execute(stmt)
        await self.session.commit()
