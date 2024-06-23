from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database.repo.request import Request
from keyboards import learning_words_kb, learning_words_after_the_response_kb
from utils.random_words import get_random_words, set_states, get_words_for_kb
from utils.states import LearningWordState

router = Router(name=__name__)


@router.message(StateFilter(None), F.text == "📖 Повторить слова")
async def repeat_words(message: Message, request: Request):
    deta = await request.words.get_new_word_in_user_words(message.from_user.id)
    if deta is None:
        print('no words')
    else:
        print(deta.in_english, deta.in_russian)


@router.message(StateFilter(None), F.text == "📝 Учить новые слова")
async def new_words(message: Message, state: FSMContext, request: Request):
    data = await get_random_words(message, request)
    if data is None:
        return message.answer(f"Слова для изучения закончились!\n"
                              f"Вы можете повторить изученные слова.")
    await set_states(state=state, data=data)
    await state.update_data(type_learning="new_")
    kb = await learning_words_kb(prefix="new_", words=get_words_for_kb(data))
    await message.answer(
        text=f"<b>Выберите правильный перевод:</b>\n{data['ru_correct']}",
        reply_markup=kb)


@router.callback_query(
    F.data.startswith("new_") | F.data.startswith("repeat_") | F.data.startswith("random_"),
    StateFilter(LearningWordState))
async def learning_words(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    kb = await learning_words_after_the_response_kb()
    prefix = data['type_learning']
    if callback.data.replace(prefix, "") == data['en_correct']:
        await callback.answer("Верно!")
        await callback.message.edit_text(
            f"<b>Верно! Правильный перевод:</b>\n{data['en_correct']}",
            reply_markup=kb)
    else:
        await callback.answer("Не верно!")
        await callback.message.edit_text(
            f"<b>Не верно! Правильный перевод:</b>\n{data['en_correct']}",
            reply_markup=kb)


@router.callback_query(F.data.startswith("answer_"))
async def answer_to_the_choice(callback: CallbackQuery, state: FSMContext, request: Request):
    if callback.data.replace("answer_", "") == "finish":
        await state.clear()
        return await callback.message.edit_text("Хорошо позанимались!", reply_markup=None)
    elif callback.data.replace("answer_", "") == "remember":
        data = await get_random_words(callback, request)
        await set_states(state=state, data=data)
        kb = await learning_words_kb(prefix="new_", words=get_words_for_kb(data))
        await callback.answer("Слово добавлено в словарь")
        await callback.message.edit_text(
            text=f"<b>Выберите правильный перевод:</b>\n{data['ru_correct']}",
            reply_markup=kb)
    else:
        data = await get_random_words(callback, request)
        await set_states(state=state, data=data)
        kb = await learning_words_kb(prefix="new_", words=get_words_for_kb(data))
        await callback.answer("Слово будет показано снова")
        await callback.message.edit_text(
            f"<b>Выберите правильный перевод:</b>\n{data['ru_correct']}",
            reply_markup=kb)
