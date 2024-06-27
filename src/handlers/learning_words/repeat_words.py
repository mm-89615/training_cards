from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message

from database.repo import Request

router = Router(name=__name__)


@router.message(StateFilter(None), F.text == "📖 Повторить слова")
async def repeat_words(message: Message, request: Request):
    deta = await request.words.get_new_word_in_user_words(message.from_user.id)
    if deta is None:
        print('no words')
    else:
        print(deta.in_english, deta.in_russian)
