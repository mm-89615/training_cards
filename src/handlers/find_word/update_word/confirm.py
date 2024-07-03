from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from database.repo import Request
from keyboards import CommonKb
from utils.states import DictType
from utils.states import FindWordState

router = Router(name=__name__)


@router.message(StateFilter(FindWordState.confirm), F.text == CommonKb.yes)
async def add_word_confirm_yes(message: Message, state: FSMContext, request: Request):
    data = await state.get_data()
    if data["dict_type"] == DictType.admin:
        await request.words.update_word(
            word_id=data["word_id"], in_english=data["en"], in_russian=data["ru"]
        )
    elif data["dict_type"] == DictType.user:
        await request.user_words.update_word(
            word_id=data["word_id"],
            in_english=data["en"],
            in_russian=data["ru"],
            tg_id=message.from_user.id,
        )
    await message.answer("Слово обновлено!", reply_markup=ReplyKeyboardRemove())
    await state.clear()


@router.message(StateFilter(FindWordState.confirm), F.text == CommonKb.no)
async def add_word_confirm_no(message: Message, state: FSMContext):
    await message.answer("Слово не обновлено!", reply_markup=ReplyKeyboardRemove())
    await state.clear()


@router.message(StateFilter(FindWordState.confirm))
async def add_word_confirm_incorrect(message: Message):
    await message.answer(
        text="Выберите предложенный вариант из меню.",
        reply_markup=CommonKb.yes_or_no_kb(),
    )
