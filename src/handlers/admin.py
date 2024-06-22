from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from filters import IsAdmin
from keyboards import admin_kb

router = Router(name=__name__)
# router.message.filter()


@router.message(F.text.in_(["⚙️ Админ панель", "/admin_panel"]))
async def admin_panel(message: Message):
    kb = await admin_kb()
    return message.answer(f"Выберите действие", reply_markup=kb)


@router.message(F.text.in_(["➕ Добавить слово", "/add_word"]))
async def add_word(message: Message):
    return message.answer(f"Слово добавлено!")


@router.message(F.text.in_(["➖ Изменить слово", "/change_word"]))
async def change_word(message: Message):
    return message.answer(f"Слово изменено!")


@router.message(F.text.in_(["✖️ Удалить слово", "/delete_word"]))
async def delete_word(message: Message):
    return message.answer(f"Слово удалено!")
