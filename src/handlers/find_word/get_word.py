from aiogram import Router, F
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from filters import IsAdmin
from keyboards import AdminKb, UserKb
from utils.states import DictType, FindWordState

router = Router(name=__name__)


@router.message(StateFilter(None), Command(commands=["find"], prefix="!"), IsAdmin())
@router.message(F.text == AdminKb.find_word)
async def add_word(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(FindWordState.dict_type)
    await state.update_data(dict_type=DictType.admin)
    await message.answer(
        text=f"Введите значение слова на английском языке: ",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(StateFilter(None), Command(commands=["find"]))
@router.message(F.text == UserKb.find_word)
async def add_word(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(FindWordState.dict_type)
    await state.update_data(dict_type=DictType.user)
    await message.answer(
        text=f"Введите значение слова на английском языке: ",
        reply_markup=ReplyKeyboardRemove(),
    )
