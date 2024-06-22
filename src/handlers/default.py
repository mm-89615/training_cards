from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from database.requests import Requests
from keyboards import start_kb

router = Router(name=__name__)


@router.message(CommandStart())
async def start(message: Message, request: Requests):
    await request.users.get_or_create_user(
        tg_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )
    kb = await start_kb(message)
    return message.answer(f"Добро пожаловать, {message.from_user.first_name}!", reply_markup=kb)


@router.message(Command("about"))
async def about(message: Message):
    return message.answer("О проекте")
