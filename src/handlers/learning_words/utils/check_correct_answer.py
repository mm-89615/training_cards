from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup


async def check_correct_answer(callback: CallbackQuery, state: FSMContext, prefix: str,
                               kb: InlineKeyboardMarkup):
    data = await state.get_data()
    if callback.data.replace(prefix, "") == data['en_correct']:
        await callback.answer("Верно!", cache_time=1)
        await callback.message.edit_text(
            f"<b>Верно! Правильный перевод:</b>\n{data['en_correct']}",
            reply_markup=kb)
    else:
        await callback.answer("Не верно!", cache_time=1)
        await callback.message.edit_text(
            f"<b>Не верно! Правильный перевод:</b>\n{data['en_correct']}",
            reply_markup=kb)
    await state.update_data(count_words=(data["count_words"] + 1))
