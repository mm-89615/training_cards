from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database.repo import Request
from utils.states import LearningWordState


async def get_random_words(msg: Message | CallbackQuery, request: Request):
    find_word = await request.words.get_new_word_not_in_user_words(msg.from_user.id)
    other_words = await request.words.get_random_words(find_word.id)
    data = {
        "ru_correct": find_word.in_russian,
        "en_correct": find_word.in_english,
        "incorrect": {word.in_english: word.in_russian for word in other_words}
    }
    return data


def get_words_for_kb(data: dict[str, str]):
    kb = {
        data["en_correct"]: data["ru_correct"],
        **data["incorrect"]
    }
    return kb


async def set_states(state: FSMContext, data: dict[str, str]):
    await state.set_state(LearningWordState.start)
    await state.update_data(en_correct=data["en_correct"],
                            ru_correct=data["ru_correct"],
                            incorrect=data["incorrect"])
