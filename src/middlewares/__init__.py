__all__ = "register_global_middlewares"

from aiogram import Dispatcher

from database import async_session
from .database import DatabaseMiddleware


def register_global_middlewares(dp: Dispatcher):
    dp.update.middleware(DatabaseMiddleware(async_session))
