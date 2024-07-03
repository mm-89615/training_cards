from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery


async def cancel_callback(
    callback: CallbackQuery, state: FSMContext, data: dict[str, str]
):
    await state.clear()
    await callback.message.edit_text(
        text=f"Хорошо позанимались!\nВы повторили слов: {data['count_words']}",
        reply_markup=None,
    )
