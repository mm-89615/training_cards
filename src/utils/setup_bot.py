import logging
from typing import List

from aiogram import Bot


async def on_startup(bot: Bot, admin_ids: List[int]):
    for admin in admin_ids:
        await bot.send_message(chat_id=admin, text="Бот запущен!")
    logging.warning("Бот запущен!")


async def on_shutdown(bot: Bot, admin_ids: List[int]):
    for admin in admin_ids:
        await bot.send_message(chat_id=admin, text="Бот остановлен!")
