from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.states import DictType


class FindCallback(CallbackData, prefix="find"):
    dict_type: DictType
    level: int
    find_word: str | None = None
    user_id: int | None = None
    action: str | None = None
    word_id: int | None = None
    page: int | None = 1


def get_words_buttons(
    level: int,
    dict_type: DictType,
    find_word: str,
    user_id: int,
    page: int,
    paginator_buttons: dict,
    words_on_page: list,
):
    keyboard = InlineKeyboardBuilder()
    for button in words_on_page:
        keyboard.add(
            InlineKeyboardButton(
                text=f"{button.in_english}",
                callback_data=FindCallback(
                    dict_type=dict_type,
                    level=level + 1,
                    find_word=find_word,
                    user_id=user_id,
                    page=page,
                    word_id=button.id,
                ).pack(),
            )
        )
    keyboard.adjust(
        2,
    )

    row = []

    for text, action in paginator_buttons.items():
        if action == "next":
            row.append(
                InlineKeyboardButton(
                    text=text,
                    callback_data=FindCallback(
                        dict_type=dict_type,
                        level=level,
                        find_word=find_word,
                        user_id=user_id,
                        page=page + 1,
                    ).pack(),
                )
            )
        elif action == "previous":
            row.append(
                InlineKeyboardButton(
                    text=text,
                    callback_data=FindCallback(
                        dict_type=dict_type,
                        level=level,
                        find_word=find_word,
                        user_id=user_id,
                        page=page - 1,
                    ).pack(),
                )
            )
    keyboard.row(*row)
    keyboard.row(
        InlineKeyboardButton(
            text="❌ Выйти",
            callback_data=FindCallback(
                dict_type=dict_type, level=level, action="exit"
            ).pack(),
        )
    )
    return keyboard.as_markup()


def get_word_actions_kb(
    dict_type: DictType,
    level: int,
    page: int,
    find_word: str,
    user_id: int,
    word_id: int,
):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text="❌ Удалить",
            callback_data=FindCallback(
                dict_type=dict_type,
                level=level + 1,
                word_id=word_id,
                find_word=find_word,
                user_id=user_id,
                page=page,
            ).pack(),
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text="📝 Редактировать",
            callback_data=FindCallback(
                dict_type=dict_type,
                level=level,
                word_id=word_id,
                action="edit",
                find_word=find_word,
                user_id=user_id,
                page=page,
            ).pack(),
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text="⬅️ Назад",
            callback_data=FindCallback(
                dict_type=dict_type,
                level=level - 1,
                find_word=find_word,
                user_id=user_id,
                page=page,
            ).pack(),
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text="⭕ Выйти",
            callback_data=FindCallback(
                dict_type=dict_type, level=level, action="exit"
            ).pack(),
        )
    )
    keyboard.adjust(
        2,
    )

    return keyboard.as_markup()


def get_confirm_delete_kb(
    dict_type: DictType,
    level: int,
    page: int,
    find_word: str,
    user_id: int,
    word_id: int,
):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text="✅ Да",
            callback_data=FindCallback(
                dict_type=dict_type,
                level=0,
                find_word=find_word,
                action="delete",
                word_id=word_id,
                user_id=user_id,
                page=page,
            ).pack(),
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text="❌ Нет",
            callback_data=FindCallback(
                dict_type=dict_type,
                level=level - 1,
                find_word=find_word,
                word_id=word_id,
                user_id=user_id,
                page=page,
            ).pack(),
        )
    )

    keyboard.adjust(
        2,
    )

    return keyboard.as_markup()


def exit_kb():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text="❌ Выйти",
            callback_data=FindCallback(
                dict_type=DictType.user, level=0, action="exit"
            ).pack(),
        )
    )
    return keyboard.as_markup()
