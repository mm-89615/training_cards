from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database.repo import Request
from keyboards import learning_words_kb, ChoiceActionsKb
from utils.states import TypeLearning, LearningWordState
from .utils import get_words_for_kb, check_correct_answer, GetData, set_new_state, update_state
from .utils.cancel_callback import cancel_callback

router = Router(name=__name__)


@router.message(StateFilter(None), F.text == "🔁 Случайные слова")
async def get_random_words(message: Message, state: FSMContext, request: Request):
    data = await GetData.random_words(message, request)
    if data is None:
        return await message.answer("К сожалению, слов нет")
    await set_new_state(state=state, data=data, type_learning=TypeLearning.random_)
    kb = learning_words_kb(prefix=TypeLearning.random_, words=get_words_for_kb(data))
    await message.answer(
        text=f"<b>Выберите правильный перевод:</b>\n{data['ru_correct']}",
        reply_markup=kb
    )

@router.callback_query(F.data.startswith(TypeLearning.random_))
async def correct_answer(callback: CallbackQuery, state: FSMContext):
    kb = ChoiceActionsKb.random_()
    await check_correct_answer(callback=callback, state=state, prefix=TypeLearning.random_, kb=kb)




