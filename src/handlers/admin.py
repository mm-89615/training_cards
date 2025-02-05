from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from filters import IsAdmin
from keyboards import AdminKb, StartKb

router = Router(name=__name__)
router.message.filter(IsAdmin())


@router.message(Command("admin"))
@router.message(F.text == StartKb.admin_panel)
async def admin(message: Message):
    kb = AdminKb.get_kb()
    await message.answer("Выберите пункт меню", reply_markup=kb)
