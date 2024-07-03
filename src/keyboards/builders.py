from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


class Builder:
    @staticmethod
    def reply(
        buttons: list[str],
        size: tuple = (1,),
        resize_keyboard: bool = True,
        one_time_keyboard: bool = True,
        placeholder: str = None,
        is_persistent: bool = False,
    ) -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardBuilder()
        for button in buttons:
            keyboard.add(KeyboardButton(text=str(button)))
        keyboard.adjust(*size)
        return keyboard.as_markup(
            resize_keyboard=resize_keyboard,
            one_time_keyboard=one_time_keyboard,
            input_field_placeholder=placeholder,
            is_persistent=is_persistent,
        )

    @staticmethod
    def inline(
        buttons: dict,
        size: tuple = (1,),
        resize_keyboard: bool = True,
        one_time_keyboard: bool = True,
    ) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardBuilder()
        for button in buttons:
            keyboard.add(
                InlineKeyboardButton(text=str(button), callback_data=buttons[button])
            )
        keyboard.adjust(*size)
        return keyboard.as_markup(
            resize_keyboard=resize_keyboard, one_time_keyboard=one_time_keyboard
        )
