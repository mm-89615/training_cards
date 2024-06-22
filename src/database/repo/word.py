from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from .base import BaseRequest
from ..models import Word


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
