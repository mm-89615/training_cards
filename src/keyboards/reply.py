from aiogram.types import Message

from config import settings
from .builders import Builder


class CommonKb:
    yes = "✅ Да"
    no = "❌ Нет"

    @staticmethod
    def yes_or_no_kb():
        kb = [
            CommonKb.yes,
            CommonKb.no
        ]
        return Builder.reply(buttons=kb, size=(2,), one_time_keyboard=True)


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
            StartKb.words_panel
        ]
        if message.from_user.id in settings.bot.admin_ids:
            kb.append("⚙️ Админ панель")
        return Builder.reply(buttons=kb, size=(1, 1, 1, 2), one_time_keyboard=True)


class AdminKb:
    add_word = "✅ Добавить слово"
    find_word = "🔎 Найти слово"

    @staticmethod
    def get_kb():
        kb = [
            AdminKb.add_word,
            AdminKb.find_word,
        ]
        return Builder.reply(buttons=kb, size=(2,), one_time_keyboard=True)


class UserKb:
    add_word = "✅ Добавить новое слово"
    find_word = "🔍 Найти слово"

    @staticmethod
    def get_kb():
        kb = [
            UserKb.add_word,
            UserKb.find_word,
        ]
        return Builder.reply(buttons=kb, size=(2,), one_time_keyboard=True)


def get_word_kb(word):
    kb = [word]
    return Builder.reply(buttons=kb, size=(1,), one_time_keyboard=True)
