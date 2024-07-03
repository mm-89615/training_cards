import random

from .builders import Builder


def learning_words_kb(prefix: str, words: dict[str, str]):
    kb = {}
    keys = list(words.items())
    random.shuffle(keys)
    shuffled_words = dict(keys)
    for word in shuffled_words:
        kb[word] = f"{prefix}{word}"
    return Builder.inline(buttons=kb, size=(2, 2))


class ChoiceActionsKb:
    prefix = "action_"
    add_to_yourself = ("✅ Добавить себе!", f"{prefix}add")
    skip = ("➡️ Пропустить", f"{prefix}skip")
    next = ("➡️ Следующее слово", f"{prefix}next")
    remember = ("✅ Запомнил", f"{prefix}remember")
    not_remember = ("🔁 Повторить еще", f"{prefix}not_remember")
    cancel = ("❌ Закончить", f"{prefix}cancel")

    @staticmethod
    def new_():
        kb = {
            ChoiceActionsKb.add_to_yourself[0]: ChoiceActionsKb.add_to_yourself[1],
            ChoiceActionsKb.skip[0]: ChoiceActionsKb.skip[1],
            ChoiceActionsKb.cancel[0]: ChoiceActionsKb.cancel[1],
        }
        return Builder.inline(buttons=kb, size=(2, 1), one_time_keyboard=True)

    @staticmethod
    def repeat_():
        kb = {
            ChoiceActionsKb.remember[0]: ChoiceActionsKb.remember[1],
            ChoiceActionsKb.not_remember[0]: ChoiceActionsKb.not_remember[1],
            ChoiceActionsKb.cancel[0]: ChoiceActionsKb.cancel[1],
        }
        return Builder.inline(buttons=kb, size=(2, 1), one_time_keyboard=True)

    @staticmethod
    def random_():
        kb = {
            ChoiceActionsKb.next[0]: ChoiceActionsKb.next[1],
            ChoiceActionsKb.cancel[0]: ChoiceActionsKb.cancel[1],
        }
        return Builder.inline(buttons=kb, size=(1, 1), one_time_keyboard=True)
