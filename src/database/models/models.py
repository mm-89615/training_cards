from typing import Optional

from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

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
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    word_id: Mapped[int] = mapped_column(ForeignKey("words.id", ondelete="CASCADE"))
    repetition_counter: Mapped[int] = mapped_column(server_default="0")
