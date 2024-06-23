from aiogram.fsm.state import StatesGroup, State


class LearningWordState(StatesGroup):
    type_learning = State()
    en_correct = State()
    ru_correct = State()
    incorrect = State()
