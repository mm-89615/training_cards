from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from database.repo import Request
from keyboards import CommonKb
from utils.states import AddWordState, DictType

router = Router(name=__name__)


@router.message(StateFilter(AddWordState.confirm), F.text == CommonKb.yes)
async def add_word_confirm_yes(message: Message, state: FSMContext, request: Request):
    data = await state.get_data()
    if data["dict_type"] == DictType.admin:
        await request.words.add_word(in_english=data["en"], in_russian=data["ru"])
        await message.answer(
            "Слово добавлено в общий словарь!", reply_markup=ReplyKeyboardRemove()
        )
    elif data["dict_type"] == DictType.user:
        await request.user_words.add_user_word(
            user_id=message.from_user.id,
            word_id=None,
            in_english=data["en"],
            in_russian=data["ru"],
        )
        await message.answer(
            "Слово добавлено в ваш словарь!", reply_markup=ReplyKeyboardRemove()
        )
    await state.clear()


@router.message(StateFilter(AddWordState.confirm), F.text == CommonKb.no)
async def add_word_confirm_no(message: Message, state: FSMContext):
    await message.answer("Слово не добавлено", reply_markup=ReplyKeyboardRemove())
    await state.clear()


@router.message(StateFilter(AddWordState.confirm))
async def add_word_confirm_incorrect(message: Message):
    await message.answer(
        text="Выберите предложенный вариант из меню.",
        reply_markup=CommonKb.yes_or_no_kb(),
    )
