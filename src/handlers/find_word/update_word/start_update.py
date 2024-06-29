from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database.models import Word
from database.repo import Request
from keyboards import get_word_kb
from utils.states import DictType, FindWordState
from ..callback.buttons import FindCallback

router = Router(name=__name__)


@router.callback_query(FindCallback.filter(F.action == "edit"))
async def edit_word(callback: CallbackQuery, callback_data: FindCallback, request: Request,
                    state: FSMContext):
    word = Word
    if callback_data.dict_type == DictType.admin:
        word = await request.words.get_word_by_id(word_id=callback_data.word_id)
    elif callback_data.dict_type == DictType.user:
        word = await request.user_words.get_word_by_id(word_id=callback_data.word_id, tg_id=callback_data.user_id)
    await state.update_data(word_id=word.id, old_en=word.in_english, old_ru=word.in_russian)
    kb = get_word_kb(word.in_english)
    await callback.message.delete()
    await callback.message.answer("Введите новое значение слова на английском языке: ", reply_markup=kb)
    await state.set_state(FindWordState.en)
