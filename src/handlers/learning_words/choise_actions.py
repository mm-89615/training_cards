from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.repo import Request
from handlers.learning_words.utils import GetData, update_state, get_words_for_kb
from handlers.learning_words.utils.cancel_callback import cancel_callback
from keyboards import ChoiceActionsKb, learning_words_kb
from utils.states import TypeLearning

router = Router(name=__name__)


class ChoiceActions:

    @staticmethod
    async def new_(state: FSMContext, request: Request, callback: CallbackQuery, old_data: dict[str, str]):
        if callback.data == ChoiceActionsKb.cancel[1]:
            return await cancel_callback(callback=callback, state=state, data=old_data)
        data = await GetData.new_words(callback, request)
        await update_state(state=state, data=data)
        kb = learning_words_kb(prefix=TypeLearning.new_, words=get_words_for_kb(data))
        if callback.data == ChoiceActionsKb.add_to_yourself[1]:
            await callback.answer("Слово добавлено в словарь")
            await callback.message.edit_text(
                text=f"<b>Выберите правильный перевод:</b>\n{data['ru_correct']}",
                reply_markup=kb)
        elif callback.data == ChoiceActionsKb.skip[1]:
            await callback.answer("Слово будет показано снова")
            await callback.message.edit_text(
                f"<b>Выберите правильный перевод:</b>\n{data['ru_correct']}",
                reply_markup=kb)

    @staticmethod
    async def random_(state: FSMContext, request: Request, callback: CallbackQuery, old_data: dict[str, str]):
        if callback.data == ChoiceActionsKb.cancel[1]:
            return await cancel_callback(callback=callback, state=state, data=old_data)
        data = await GetData.random_words(callback, request)
        await update_state(state=state, data=data)
        kb = learning_words_kb(prefix=TypeLearning.random_, words=get_words_for_kb(data))
        if callback.data == ChoiceActionsKb.next[1]:
            await callback.answer("Следующее слово")
            await callback.message.edit_text(
                text=f"<b>Выберите правильный перевод:</b>\n{data['ru_correct']}",
                reply_markup=kb)

    @staticmethod
    async def repeat_(state: FSMContext, request: Request, callback: CallbackQuery, old_data: dict[str, str]):
        if callback.data == ChoiceActionsKb.cancel[1]:
            return await cancel_callback(callback=callback, state=state, data=old_data)
        data = await GetData.repeat_words(callback, request)
        await update_state(state=state, data=data)
        kb = learning_words_kb(prefix=TypeLearning.repeat_, words=get_words_for_kb(data))
        if callback.data == ChoiceActionsKb.remember[1]:
            await callback.answer("Отлично!")
            await callback.message.edit_text(
                text=f"<b>Выберите правильный перевод:</b>\n{data['ru_correct']}",
                reply_markup=kb)
        elif callback.data == ChoiceActionsKb.not_remember[1]:
            await callback.answer("Слово будет показано еще!")
            await callback.message.edit_text(
                f"<b>Выберите правильный перевод:</b>\n{data['ru_correct']}",
                reply_markup=kb)


@router.callback_query(F.data.startswith(ChoiceActionsKb.prefix))
async def choosing_actions(callback: CallbackQuery, state: FSMContext, request: Request):
    old_data = await state.get_data()
    if old_data["type_learning"] == TypeLearning.new_:
        return await ChoiceActions.new_(state=state, request=request, callback=callback, old_data=old_data)
    elif old_data["type_learning"] == TypeLearning.repeat_:
        return await ChoiceActions.repeat_(state=state, request=request, callback=callback, old_data=old_data)
    elif old_data["type_learning"] == TypeLearning.random_:
        return await ChoiceActions.random_(state=state, request=request, callback=callback, old_data=old_data)
