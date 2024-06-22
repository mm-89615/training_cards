from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards import start_kb

router = Router(name=__name__)


@router.message()
async def start_cmd(message: Message):
    kb = await start_kb(message)
    return message.answer(f"Добро пожаловать, {message.from_user.first_name}!", reply_markup=kb)
