from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from filters import RussianText
from keyboards import CommonKb
from utils.states import AddWordState, DictType

router = Router(name=__name__)


@router.message(StateFilter(AddWordState.ru), RussianText())
async def add_word_ru(message: Message, state: FSMContext):
    await state.update_data(ru=message.text)
    data = await state.get_data()
    text = (
        f"Перевод на английском: \n"
        f"<b>{data['en']}</b>\n\n"
        f"Перевод на русский: \n"
        f"<b>{data['ru']}</b>\n\n"
    )
    if data["dict_type"] == DictType.admin:
        text += "Добавить данное сочетание в общий словарь?"
    elif data["dict_type"] == DictType.user:
        text += "Добавить данное сочетание в ваш словарь?"
    await message.answer(text=text, reply_markup=CommonKb.yes_or_no_kb())
    await state.set_state(AddWordState.confirm)


@router.message(StateFilter(AddWordState.ru))
async def add_word_ru_incorrect(message: Message):
    await message.answer(
        f"Убедитесь что правильно ввели слово!\n"
        f"Доступны буквы русского алфавита и символы: <b>, . ? ( ) - </b>\n"
        f"Попробуйте ещё раз ввести слово русском языке: "
    )
