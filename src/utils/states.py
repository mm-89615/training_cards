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
