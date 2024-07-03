from aiogram.types import Message

from config import settings
from .builders import Builder


class CommonKb:
    yes = "✅ Да"
    no = "❌ Нет"

    @staticmethod
    def yes_or_no_kb():
        kb = [CommonKb.yes, CommonKb.no]
        placeholder = "Выберите пункт меню: "
        return Builder.reply(buttons=kb, size=(2,), placeholder=placeholder)


class StartKb:
    new_word = "📝 Учить новые слова"
    repeat_words = "📖 Повторить слова"
    random_words = "🔁 Случайные слова"
    words_panel = "📚 Управление словами"
    admin_panel = "⚙️ Админ панель"

    @staticmethod
    def get_kb(message: Message):
        kb = [
            StartKb.new_word,
            StartKb.repeat_words,
            StartKb.random_words,
            StartKb.words_panel,
        ]
        if message.from_user.id in settings.bot.admin_ids:
            kb.append("⚙️ Админ панель")
        placeholder = "Выберите пункт меню: "
        return Builder.reply(buttons=kb, size=(1, 1, 1, 2), placeholder=placeholder)


class AdminKb:
    add_word = "✅ Добавить слово"
    find_word = "🔎 Найти слово"

    @staticmethod
    def get_kb():
        kb = [
            AdminKb.add_word,
            AdminKb.find_word,
        ]
        placeholder = "Выберите пункт меню: "
        return Builder.reply(buttons=kb, size=(2,), placeholder=placeholder)


class UserKb:
    add_word = "✅ Добавить новое слово"
    find_word = "🔍 Найти слово"

    @staticmethod
    def get_kb():
        kb = [
            UserKb.add_word,
            UserKb.find_word,
        ]
        placeholder = "Выберите пункт меню: "
        return Builder.reply(buttons=kb, size=(2,), placeholder=placeholder)


def get_word_kb(word):
    kb = [word]
    placeholder = "Нажмите на слово, если не хотите менять: "
    return Builder.reply(buttons=kb, size=(1,), placeholder=placeholder)
