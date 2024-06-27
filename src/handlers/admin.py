from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from filters import IsAdmin
from keyboards import AdminKb, StartKb

router = Router(name=__name__)
router.message.filter(IsAdmin())


@router.message(Command(commands=["admin"], prefix="!"))
@router.message(F.text == StartKb.admin_panel)
async def admin_panel(message: Message):
    kb = AdminKb.get_kb()
    await message.answer(f"Выберите действие", reply_markup=kb)


@router.message(Command(commands=["add_word"], prefix="!"))
@router.message(F.text == AdminKb.add_word)
async def add_word(message: Message):
    await message.answer(f"Слово добавлено!")


@router.message(Command(commands=["change_word"], prefix="!"))
@router.message(F.text == AdminKb.change_word)
async def change_word(message: Message):
    await message.answer(f"Слово изменено!")


@router.message(Command(commands=["delete_word"], prefix="!"))
@router.message(F.text == AdminKb.delete_word)
async def delete_word(message: Message):
    await message.answer(f"Слово удалено!")
