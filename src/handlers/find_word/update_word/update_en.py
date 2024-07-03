from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from filters import EnglishText
from keyboards import get_word_kb
from utils.states import FindWordState

router = Router(name=__name__)


@router.message(StateFilter(FindWordState.en), EnglishText())
async def update_word_en(message: Message, state: FSMContext):
    await state.update_data(en=message.text)
    data = await state.get_data()
    kb = get_word_kb(data["old_ru"])
    await message.answer(
        "Введите новое значение слова на русском языке: ", reply_markup=kb
    )
    await state.set_state(FindWordState.ru)


@router.message(StateFilter(FindWordState.en))
async def get_word_en_incorrect(message: Message):
    await message.answer(
        f"Убедитесь что правильно ввели слово!\n"
        f"Доступны буквы английского алфавита и символы: <b>' , . ? ( ) - </b> \n"
        f"Попробуйте ещё раз ввести слово на английском языке: "
    )
