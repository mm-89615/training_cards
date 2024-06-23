from aiogram.fsm.state import StatesGroup, State


class LearningNewWordState(StatesGroup):
    en_correct = State()
    ru_correct = State()
    incorrect = State()
