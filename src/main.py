import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import settings
from middlewares import register_global_middlewares
from utils import setup_logging, on_startup, on_shutdown


async def main():
    setup_logging()

    bot = Bot(
        token=settings.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()

    register_global_middlewares(dp)

    await bot.delete_webhook(drop_pending_updates=True)
    await on_startup(bot, settings.bot.admin_ids)
    await on_shutdown(bot, settings.bot.admin_ids)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Бот остановлен!")
