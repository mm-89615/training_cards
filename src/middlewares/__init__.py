__all__ = (
    "register_global_middlewares"
)

from aiogram import Dispatcher

from config import settings
from database import async_session
from .database import DatabaseMiddleware
from .settings import ConfigMiddleware


def register_global_middlewares(dp: Dispatcher):
    dp.update.middleware(ConfigMiddleware(settings))
    dp.update.middleware(DatabaseMiddleware(async_session))
