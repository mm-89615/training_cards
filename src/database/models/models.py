from typing import Optional

from select import select
from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import IntIdPkMixin, TimestampMixin


class User(IntIdPkMixin, TimestampMixin, Base):
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    username: Mapped[str]
    first_name: Mapped[Optional[str]]
    last_name: Mapped[Optional[str]]


class Word(IntIdPkMixin, TimestampMixin, Base):
    in_russian: Mapped[str] = mapped_column(String(255))
    in_english: Mapped[str] = mapped_column(String(100))


class UserWord(IntIdPkMixin, TimestampMixin, Base):
    user_tg_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.tg_id", ondelete="CASCADE")
    )
    word_id: Mapped[int | None] = mapped_column(
        ForeignKey("words.id", ondelete="CASCADE")
    )
    in_russian: Mapped[str | None] = mapped_column(String(255))
    in_english: Mapped[str | None] = mapped_column(String(100))
    repetition_counter: Mapped[int] = mapped_column(server_default="0")

    word: Mapped[Word | None] = relationship(backref="user_words")
    user: Mapped[User] = relationship(backref="user_words")

    def __init__(self):
        super().__init__()
        if self.word_id:
            word = select(Word).where(Word.id == self.word_id).scalar_one()
            self.in_russian = word.in_russian
            self.in_english = word.in_english
