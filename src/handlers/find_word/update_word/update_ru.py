from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database.repo import Request
from filters import RussianText
from keyboards import CommonKb
from utils.states import FindWordState

router = Router(name=__name__)


@router.message(StateFilter(FindWordState.ru), RussianText())
async def update_word_ru(message: Message, state: FSMContext):
    await state.update_data(ru=message.text)
    data = await state.get_data()
    text = (f"Заменено: \n"
            f"{data['old_en']}\n"
            f"{data['old_ru']}\n\n"
            f"На: \n"
            f"{data['en']}\n"
            f"{data['ru']}\n\n"
            f"Обновить сочетание?")
    await message.answer(text=text, reply_markup=CommonKb.yes_or_no_kb())
    await state.set_state(FindWordState.confirm)


@router.message(StateFilter(FindWordState.ru))
async def add_word_ru_incorrect(message: Message):
    await message.answer(f"Убедитесь что правильно ввели слово!\n"
                         f"Доступны буквы русского алфавита и символы: <b>, . ? ( ) - </b>\n"
                         f"Попробуйте ещё раз ввести слово русском языке: ")
