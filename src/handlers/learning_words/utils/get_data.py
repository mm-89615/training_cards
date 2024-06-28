from typing import Union, Optional

from aiogram.types import Message, CallbackQuery

from database.repo import Request


class GetData:
    @staticmethod
    async def new_words(message: Union[Message, CallbackQuery], request: Request):
        find_word = await request.words.get_new_word_not_in_user_words(message.from_user.id)
        if find_word is None:
            return
        other_words = await request.words.get_three_random_words(find_word.id)
        data = {
            "en_correct": find_word.in_english,
            "ru_correct": find_word.in_russian,
            "id_correct": find_word.id,
            "incorrect": {word.in_english: word.in_russian for word in other_words}
        }
        return data

    @staticmethod
    async def repeat_words(message: Union[Message, CallbackQuery], request: Request):
        find_word = await request.user_words.get_new_word_from_user_words(message.from_user.id)
        if find_word is None:
            return
        other_words = await request.words.get_three_random_words(find_word.word_id)
        data = {
            "en_correct": find_word.in_english,
            "ru_correct": find_word.in_russian,
            "id_correct": find_word.id,
            "repetitions": find_word.repetition_counter,
            "incorrect": {word.in_english: word.in_russian for word in other_words}
        }
        return data

    @staticmethod
    async def random_words(message: Union[Message, CallbackQuery], request: Request):
        words = await request.words.get_four_random_words(message.from_user.id)
        if words is None:
            return
        data = {
            "en_correct": words[0].in_english,
            "ru_correct": words[0].in_russian,
            "id_correct": words[0].id,
            "incorrect": {word.in_english: word.in_russian for word in words[1:]}
        }
        return data
