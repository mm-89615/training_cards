from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database.repo import Request
from keyboards import learning_words_kb, ChoiceActionsKb
from utils.states import TypeLearning
from .utils import set_new_state, get_words_for_kb, check_correct_answer, GetData

router = Router(name=__name__)


@router.message(StateFilter(None), F.text == "📝 Учить новые слова")
async def get_new_words(message: Message, state: FSMContext, request: Request):
    data = await GetData.new_words(message, request)
    if data is None:
        return await message.answer(f"Слова для изучения закончились!\n"
                                    f"Вы можете повторить изученные слова.")
    await set_new_state(state=state, data=data, type_learning=TypeLearning.new_)
    kb = learning_words_kb(prefix=TypeLearning.new_, words=get_words_for_kb(data))
    await message.answer(
        text=f"<b>Выберите правильный перевод:</b>\n{data['ru_correct']}",
        reply_markup=kb)


@router.callback_query(F.data.startswith(TypeLearning.new_))
async def correct_answer(callback: CallbackQuery, state: FSMContext):
    kb = ChoiceActionsKb.new_()
    await check_correct_answer(callback=callback, state=state, prefix=TypeLearning.new_, kb=kb)
