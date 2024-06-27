__all__ = ("router",)

from aiogram import Router

from .admin import router as admin_router
from .base import router as default_router
from .learning_words import router as learning_words_router

router = Router(name=__name__)

router.include_routers(
    admin_router,
    default_router,
    learning_words_router,
)
