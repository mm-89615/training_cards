from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import insert

from .base import BaseRequest
from ..models import Word, UserWord, User


class WordRequests(BaseRequest):

    async def get_words_by_english(self, english_word: str):
        stmt = select(Word).where(Word.in_english.like(english_word))
        result = await self.session.scalars(stmt)
        return result.all()

    async def add_word(self, in_english: str, in_russian: str):
        stmt = insert(Word).values(in_english=in_english, in_russian=in_russian)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one()

    async def get_all_words(self):
        stmt = select(Word).order_by(Word.id)
        result = await self.session.scalars(stmt)
        return result.all()

    async def get_random_words(self, word_id: int):
        stmt = (select(Word)
                .where(Word.id.not_in([word_id]))
                .order_by(func.random())
                .limit(3))
        result = await self.session.scalars(stmt)
        return result.all()

    async def get_new_word_not_in_user_words(self, tg_id: int):
        stmt = (select(Word)
                .where(Word.id.not_in((
                    select(UserWord.word_id)
                    .join(User).where(User.tg_id == tg_id)
                    .where(UserWord.user_id == User.id))))
                .order_by(func.random())
                .limit(1))
        result = await self.session.scalars(stmt)
        return result.one_or_none()