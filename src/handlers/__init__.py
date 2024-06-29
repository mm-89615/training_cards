__all__ = ("router",)

from aiogram import Router

from .add_word_handlers import router as add_word_router
from .admin import router as admin_router
from .base import router as default_router
from .learning_words import router as learning_words_router
from .user import router as user_router
from  .find_word import router as find_word_router
router = Router(name=__name__)

router.include_routers(
    default_router,
    admin_router,
    user_router,
    add_word_router,
    find_word_router,
    learning_words_router,
)
