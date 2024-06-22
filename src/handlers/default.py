from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from keyboards import start_kb

router = Router(name=__name__)


@router.message(CommandStart())
async def start(message: Message):
    kb = await start_kb(message)
    return message.answer(f"Добро пожаловать, {message.from_user.first_name}!", reply_markup=kb)


@router.message(Command("about"))
async def about(message: Message):
    return message.answer("О проекте")
