from database.models import Word
from database.repo import Request
from utils import Paginator
from utils.states import DictType
from .buttons import get_word_actions_kb, get_words_buttons, get_confirm_delete_kb


async def found_words(
        request: Request,
        dict_type: DictType,
        level: int,
        find_word: str,
        user_id: int,
        page: int):
    words = []
    if dict_type == DictType.admin:
        words = await request.words.get_word_by_english(find_word)
    elif dict_type == DictType.user:
        words = await request.user_words.get_word_by_english(find_word, user_id)
    if words:
        paginator = Paginator(words, page=page, per_page=6)
        words_on_page = paginator.get_page()
        paginator_buttons = pages(paginator)

        text = (f"Слов найдено: {len(words)}\n"
                f"Страница {paginator.page} из {paginator.pages}\n")

        keyboard = get_words_buttons(
            dict_type=dict_type,
            level=level,
            find_word=find_word,
            user_id=user_id,
            page=page,
            words_on_page=words_on_page,
            paginator_buttons=paginator_buttons,
        )
    else:
        text = "Совпадений не найдено!"
        keyboard = None
    return text, keyboard


def pages(paginator: Paginator):
    buttons = dict()
    if paginator.has_previous():
        buttons["⬅️ Назад"] = "previous"
    if paginator.has_next():
        buttons["Вперёд ➡️"] = "next"
    return buttons


async def word_actions(request: Request,
                       dict_type: DictType,
                       level: int,
                       word_id: int,
                       find_word: str,
                       user_id: int,
                       page: int):
    word = Word
    if dict_type == DictType.admin:
        word = await request.words.get_word_by_id(word_id)
    elif dict_type == DictType.user:
        word = await request.user_words.get_word_by_id(word_id, user_id)
    text = (f"Значение слово на английском языке: \n"
            f"{word.in_english}\n\n"
            f"Перевод на русском языка:\n"
            f"{word.in_russian}\n\n")
    keyboard = get_word_actions_kb(
        dict_type=dict_type,
        level=level,
        page=page,
        find_word=find_word,
        user_id=user_id,
        word_id=word.id,
    )
    return text, keyboard


async def confirm_delete(
        request: Request,
        dict_type: DictType,
        level: int,
        word_id: int,
        find_word: str,
        user_id: int,
        page: int
):
    text = "Вы действительно хотите удалить это слово?"
    keyboard = get_confirm_delete_kb(
        dict_type=dict_type,
        level=level,
        page=page,
        find_word=find_word,
        user_id=user_id,
        word_id=word_id
    )
    return text, keyboard


async def get_find_word_menu(
        request: Request,
        dict_type: DictType,
        level: int,
        find_word: str | None = None,
        user_id: int | None = None,
        action: str | None = None,
        page: int | None = 1,
        word_id: int | None = None):
    if level == 0:
        return await found_words(request=request,
                                 dict_type=dict_type,
                                 level=level,
                                 find_word=find_word,
                                 user_id=user_id,
                                 page=page)
    if level == 1:
        return await word_actions(request=request,
                                  dict_type=dict_type,
                                  level=level,
                                  word_id=word_id,
                                  find_word=find_word,
                                  user_id=user_id,
                                  page=page)
    if level == 2:
        return await confirm_delete(request=request,
                                    dict_type=dict_type,
                                    level=level,
                                    word_id=word_id,
                                    find_word=find_word,
                                    user_id=user_id,
                                    page=page)
