from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards import learning_words_kb, learning_words_after_the_response_kb
from utils.states import LearningNewWordState

router = Router(name=__name__)


@router.message(F.text == "📝 Учить новые слова")
async def learning_new_words(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(LearningNewWordState.en_correct)
    await state.update_data(en_correct="cat")
    await state.set_state(LearningNewWordState.ru_correct)
    await state.update_data(ru_correct="кошка")
    await state.set_state(LearningNewWordState.incorrect)
    await state.update_data(incorrect={"dog": "собака", "hello": "привет", "goodbye": "до свидания"})
    words = {
        'cat': 'кошка',
        'dog': 'собака',
        'hello': 'привет',
        'goodbye': 'до свидания'
    }
    kb = await learning_words_kb(prefix="new_", words=words)
    await message.answer("Выберите правильный перевод:", reply_markup=kb)


@router.callback_query(F.data.startswith("new_"), StateFilter(LearningNewWordState))
async def learning_new_words(callback: CallbackQuery, state: FSMContext):
    words = await state.get_data()
    kb = await learning_words_after_the_response_kb()
    if callback.data.replace("new_", "") == words['ru_correct']:
        await callback.message.edit_text(
            f"Верно! Правильный перевод: {words['ru_correct']}",
            reply_markup=kb)
    else:
        await callback.message.edit_text(
            f"Не верно! Правильный перевод: {words['ru_correct']}",
            reply_markup=kb)


@router.callback_query(F.data.startswith("answer_"))
async def answer_to_the_choice(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(LearningNewWordState.en_correct)
    await state.update_data(en_correct="cat")
    await state.set_state(LearningNewWordState.ru_correct)
    await state.update_data(ru_correct="кошка")
    await state.set_state(LearningNewWordState.incorrect)
    await state.update_data(incorrect={"dog": "собака", "hello": "привет", "goodbye": "до свидания"})
    words = {
        'cat': 'кошка',
        'dog': 'собака',
        'hello': 'привет',
        'goodbye': 'до свидания'
    }
    kb = await learning_words_kb(prefix="new_", words=words)
    if callback.data.replace("answer_", "") == "finish":
        await state.clear()
        return await callback.message.edit_text("Хорошо позанимались!", reply_markup=None)
    elif callback.data.replace("answer_", "") == "remember":
        await callback.answer("Слово добавлено в словарь")

    else:
        await callback.answer("Слово будет показано снова")
    await callback.message.edit_text("Выберите правильный перевод:", reply_markup=kb)
