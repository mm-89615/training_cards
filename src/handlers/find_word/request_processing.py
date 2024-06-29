from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database.repo import Request
from utils.states import FindWordState, DictType
from .callback.buttons import FindCallback
from .callback.find_callback import get_find_word_menu

router = Router(name=__name__)


@router.message(FindWordState.dict_type)
async def main_find(message: Message, state: FSMContext, request: Request):
    data = await state.get_data()
    text, kb = await get_find_word_menu(request=request,
                                        dict_type=data["dict_type"],
                                        level=0,
                                        find_word=message.text,
                                        user_id=message.from_user.id)
    await message.answer(text=text, reply_markup=kb)


@router.callback_query(FindCallback.filter())
async def find_word(callback: CallbackQuery, callback_data: FindCallback, request: Request):
    if callback_data.action == "delete":
        if callback_data.dict_type == DictType.admin:
            await request.words.delete_word(word_id=callback_data.word_id)
        elif callback_data.dict_type == DictType.user:
            await request.user_words.delete_word(word_id=callback_data.word_id, tg_id=callback.from_user.id)
        await callback.answer("Слово удалено!")
    text, kb = await get_find_word_menu(request=request,
                                        dict_type=callback_data.dict_type,
                                        level=callback_data.level,
                                        word_id=callback_data.word_id,
                                        find_word=callback_data.find_word,
                                        user_id=callback.from_user.id,
                                        action=callback_data.action,
                                        page=callback_data.page)
    await callback.message.edit_text(text=text, reply_markup=kb)
