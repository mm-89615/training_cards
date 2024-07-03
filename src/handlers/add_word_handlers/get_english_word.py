from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from filters import EnglishText
from utils.states import AddWordState

router = Router(name=__name__)


@router.message(StateFilter(AddWordState.en), EnglishText())
async def get_word_en(message: Message, state: FSMContext):
    await state.update_data(en=message.text)
    await message.answer(f"Введите значение слова на русском языке: ")
    await state.set_state(AddWordState.ru)


@router.message(StateFilter(AddWordState.en))
async def get_word_en_incorrect(message: Message):
    await message.answer(
        f"Убедитесь что правильно ввели слово!\n"
        f"Доступны буквы английского алфавита и символы: <b>' , . ? ( ) - </b> \n"
        f"Попробуйте ещё раз ввести слово на английском языке: "
    )
