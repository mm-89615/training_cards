from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from filters import IsAdmin
from keyboards import AdminKb, UserKb
from utils.states import AddWordState, DictType

router = Router(name=__name__)


@router.message(StateFilter(None), Command(commands=["add_word"], prefix="!"), IsAdmin())
@router.message(F.text == AdminKb.add_word)
async def add_word(message: Message, state: FSMContext):
    await state.update_data(dict_type=DictType.admin)
    await message.answer(f"Введите значение слова на английском языке: ")
    await state.set_state(AddWordState.en)


@router.message(Command(commands=["add_word"]))
@router.message(F.text == UserKb.add_word)
async def add_word(message: Message, state: FSMContext):
    await state.update_data(dict_type=DictType.user)
    await message.answer(f"Введите значение слова на английском языке: ")
    await state.set_state(AddWordState.en)
