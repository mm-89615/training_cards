from enum import StrEnum

from aiogram.fsm.state import StatesGroup, State


class TypeLearning(StrEnum):
    new_ = "new_"
    random_ = "random_"
    repeat_ = "repeat_"


class LearningWordState(StatesGroup):
    type_learning = TypeLearning
    en_correct = State()
    ru_correct = State()
    id_correct = State()
    repetitions = State()
    incorrect = State()
    count_words = State()


class DictType(StrEnum):
    admin = "admin"
    user = "user"


class AddWordState(StatesGroup):
    dict_type = State()
    en = State()
    ru = State()
    confirm = State()


class FindWordState(StatesGroup):
    dict_type = State()
    word_id = State()
    old_en = State()
    old_ru = State()
    en = State()
    ru = State()
    confirm = State()
