import random

from .builders import Builder


async def learning_words_kb(prefix: str, words: dict[str, str]):
    kb = {}
    keys = list(words.items())
    random.shuffle(keys)
    shuffled_words = dict(keys)
    for word in shuffled_words:
        kb[word] = f"{prefix}{word}"
    print(kb)
    return await Builder.inline(buttons=kb, size=(2, 2))


async def learning_words_after_the_response_kb():
    kb = {
        "✅ Добавить себе!": "answer_remember",
        "❎ Пропустить": "answer_not_remember",
        "❌ Закончить": "answer_finish",
    }
    return await Builder.inline(buttons=kb, size=(2,1), one_time_keyboard=True)
