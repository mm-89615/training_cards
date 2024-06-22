import asyncio
import logging
from typing import List

import betterlogging as bl
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import settings


async def on_startup(bot: Bot, admin_ids: List[int]):
    for admin in admin_ids:
        await bot.send_message(chat_id=admin, text="Бот запущен!")
    logging.warning("Бот запущен!")


async def on_shutdown(bot: Bot, admin_ids: List[int]):
    for admin in admin_ids:
        await bot.send_message(chat_id=admin, text="Бот остановлен!")


def setup_logging():
    logging.getLogger(__name__)
    bl.basic_colorized_config(level=logging.INFO)

    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )


async def main():
    setup_logging()

    bot = Bot(
        token=settings.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()

    await bot.delete_webhook(drop_pending_updates=True)
    await on_startup(bot, settings.bot.admin_ids)
    await on_shutdown(bot, settings.bot.admin_ids)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Бот остановлен!")
