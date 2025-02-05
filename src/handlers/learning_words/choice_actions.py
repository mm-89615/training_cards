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
    async def new_(
        state: FSMContext,
        request: Request,
        callback: CallbackQuery,
        old_data: dict[str, str],
    ):
        if callback.data == ChoiceActionsKb.cancel[1]:
            return await cancel_callback(callback=callback, state=state, data=old_data)
        if callback.data == ChoiceActionsKb.add_to_yourself[1]:
            await request.user_words.add_user_word(
                user_id=callback.from_user.id,
                word_id=int(old_data["id_correct"]),
                in_russian=old_data["ru_correct"],
                in_english=old_data["en_correct"],
            )
            await callback.answer("Слово добавлено в словарь")
        elif callback.data == ChoiceActionsKb.skip[1]:
            await callback.answer("Слово будет показано снова")
        data = await GetData.new_words(callback, request)
        if data is None:
            await callback.answer("Слова для изучения закончились!")
            return await callback.message.edit_text(
                f"Слова для изучения закончились!\n"
                f"Вы можете повторить изученные слова."
            )
        await update_state(state=state, data=data)
        kb = learning_words_kb(prefix=TypeLearning.new_, words=get_words_for_kb(data))
        await callback.message.edit_text(
            f"Выберите правильный перевод:\n\n<b>{data['ru_correct']}</b>",
            reply_markup=kb,
        )

    @staticmethod
    async def random_(
        state: FSMContext,
        request: Request,
        callback: CallbackQuery,
        old_data: dict[str, str],
    ):
        if callback.data == ChoiceActionsKb.cancel[1]:
            return await cancel_callback(callback=callback, state=state, data=old_data)
        data = await GetData.random_words(callback, request)
        await update_state(state=state, data=data)
        kb = learning_words_kb(
            prefix=TypeLearning.random_, words=get_words_for_kb(data)
        )
        if callback.data == ChoiceActionsKb.next[1]:
            await callback.answer("Следующее слово")
            await callback.message.edit_text(
                text=f"Выберите правильный перевод:\n\n<b>{data['ru_correct']}</b>",
                reply_markup=kb,
            )

    @staticmethod
    async def repeat_(
        state: FSMContext,
        request: Request,
        callback: CallbackQuery,
        old_data: dict[str, str],
    ):
        if callback.data == ChoiceActionsKb.cancel[1]:
            return await cancel_callback(callback=callback, state=state, data=old_data)
        if callback.data == ChoiceActionsKb.remember[1]:
            await request.user_words.update_number_repetitions(
                word_id=old_data["id_correct"]
            )
            await callback.answer(
                "Отлично!",
            )
        elif callback.data == ChoiceActionsKb.not_remember[1]:
            await request.user_words.update_date(word_id=old_data["id_correct"])
            await callback.answer("Слово будет показано еще!")
        data = await GetData.repeat_words(callback, request)
        if data is None:
            await callback.answer("Слова для повторения закончились!")
            return await callback.message.edit_text(
                f"Слова для повторения закончились!\n"
                f"Вы может начать учить новые слова."
            )
        await update_state(state=state, data=data)
        kb = learning_words_kb(
            prefix=TypeLearning.repeat_, words=get_words_for_kb(data)
        )
        await callback.message.edit_text(
            f"<b>Выберите правильный перевод:</b>\n\n{data['ru_correct']}",
            reply_markup=kb,
        )


@router.callback_query(F.data.startswith(ChoiceActionsKb.prefix))
async def choosing_actions(
    callback: CallbackQuery, state: FSMContext, request: Request
):
    old_data = await state.get_data()
    if old_data["type_learning"] == TypeLearning.new_:
        return await ChoiceActions.new_(
            state=state, request=request, callback=callback, old_data=old_data
        )
    elif old_data["type_learning"] == TypeLearning.repeat_:
        return await ChoiceActions.repeat_(
            state=state, request=request, callback=callback, old_data=old_data
        )
    elif old_data["type_learning"] == TypeLearning.random_:
        return await ChoiceActions.random_(
            state=state, request=request, callback=callback, old_data=old_data
        )
