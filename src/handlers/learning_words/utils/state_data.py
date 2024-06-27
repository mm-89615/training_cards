from aiogram.fsm.context import FSMContext

from utils.states import TypeLearning, LearningWordState


async def set_new_state(state: FSMContext, data: dict[str, str], type_learning: TypeLearning):
    await state.set_state(LearningWordState.type_learning)
    await state.update_data(type_learning=type_learning,
                            en_correct=data["en_correct"],
                            ru_correct=data["ru_correct"],
                            id_correct=data["id_correct"],
                            incorrect=data["incorrect"],
                            count_words=0)


async def update_state(state: FSMContext, data: dict[str, str]):
    await state.update_data(en_correct=data["en_correct"],
                            ru_correct=data["ru_correct"],
                            id_correct=data["id_correct"],
                            incorrect=data["incorrect"])
