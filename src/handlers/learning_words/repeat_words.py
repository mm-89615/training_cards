from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database.repo import Request
from handlers.learning_words.utils import GetData, set_new_state, get_words_for_kb, check_correct_answer
from keyboards import learning_words_kb, ChoiceActionsKb
from utils.states import TypeLearning

router = Router(name=__name__)


@router.message(StateFilter(None), F.text == "📖 Повторить слова")
async def get_repeat_words(message: Message, state: FSMContext, request: Request):
    data = await GetData.repeat_words(message, request)
    if data is None:
        return await message.answer(f"Слова для повторения закончились!\n"
                                    f"Вы можете начать учить новые слова или добавить свои.")
    await set_new_state(state=state, data=data, type_learning=TypeLearning.repeat_)
    kb = learning_words_kb(prefix=TypeLearning.repeat_, words=get_words_for_kb(data))
    await message.answer(
        text=f"<b>Выберите правильный перевод:</b>\n{data['ru_correct']}",
        reply_markup=kb)

@router.callback_query(F.data.startswith(TypeLearning.repeat_))
async def correct_answer(callback: CallbackQuery, state: FSMContext):
    kb = ChoiceActionsKb.repeat_()
    await check_correct_answer(callback=callback, state=state, prefix=TypeLearning.repeat_, kb=kb)
