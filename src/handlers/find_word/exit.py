from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from .callback.buttons import FindCallback

router = Router(name=__name__)


@router.callback_query(FindCallback.filter(F.action == "exit"))
async def exit_find(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Поиск завершен!")
