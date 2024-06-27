__all__ = ("router",)

from aiogram import Router

from .new_words import router as new_words_router
from .random_words import router as random_words_router
from .repeat_words import router as repeat_words_router
from .choise_actions import router as choise_actions_router
router = Router(name=__name__)
router.include_routers(
    random_words_router,
    new_words_router,
    repeat_words_router,
)
router.include_router(choise_actions_router)
