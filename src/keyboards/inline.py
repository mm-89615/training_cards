from aiogram import Bot
from aiogram.types import Message

from config import settings
from .builders import Builder


async def start_kb(message: Message):
    kb = [
        "📝 Учить новые слова",
        "📖 Повторить слова",
        "🔁 Случайные слова",
    ]

    if message.from_user.id in settings.bot.admin_ids:
        kb.append("⚙️ Админ панель")

    return await Builder.reply(buttons=kb, size=(1,))
