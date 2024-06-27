from aiogram.types import Message

from config import settings
from .builders import Builder


def start_kb(message: Message):
    kb = [
        "📝 Учить новые слова",
        "📖 Повторить слова",
        "🔁 Случайные слова",
    ]

    if message.from_user.id in settings.bot.admin_ids:
        kb.append("⚙️ Админ панель")

    return Builder.reply(buttons=kb, size=(1,), one_time_keyboard=True)


def admin_kb():
    kb = [
        "➕ Добавить слово",
        "➖ Изменить слово",
        "✖️ Удалить слово",
    ]

    return Builder.reply(buttons=kb, size=(1,), one_time_keyboard=True)


class StartKb:
    new_word = "📝 Учить новые слова"
    repeat_words = "📖 Повторить слова"
    random_words = "🔁 Случайные слова"
    admin_panel = "⚙️ Админ панель"

    @staticmethod
    def get_kb(message: Message):
        kb = [StartKb.new_word, StartKb.repeat_words, StartKb.random_words]
        if message.from_user.id in settings.bot.admin_ids:
            kb.append("⚙️ Админ панель")
        return Builder.reply(buttons=kb, size=(1,), one_time_keyboard=True)


class AdminKb:
    add_word = "➕ Добавить слово"
    change_word = "➖ Изменить слово"
    delete_word = "✖️ Удалить слово"

    @staticmethod
    def get_kb():
        kb = [AdminKb.add_word, AdminKb.change_word, AdminKb.delete_word]
        return Builder.reply(buttons=kb, size=(1,), one_time_keyboard=True)
