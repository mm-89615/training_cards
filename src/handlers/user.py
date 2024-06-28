from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from keyboards import UserKb, StartKb

router = Router(name=__name__)


@router.message(Command("words"))
@router.message(F.text == StartKb.words_panel)
async def admin(message: Message):
    kb = UserKb.get_kb()
    await message.answer("Выберите пункт меню", reply_markup=kb)
