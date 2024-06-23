from aiogram.fsm.state import StatesGroup, State


class LearningWordState(StatesGroup):
    start = State()
    en_correct = State()
    ru_correct = State()
    incorrect = State()
