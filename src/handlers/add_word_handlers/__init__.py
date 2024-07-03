__all__ = ("router",)

from aiogram import Router

from .add_word import router as add_word_router
from .confirm_stage import router as confirm_stage_router
from .get_english_word import router as get_english_word_router
from .get_russian_word import router as get_russian_word_router

router = Router(name=__name__)

router.include_routers(
    add_word_router,
    get_english_word_router,
    get_russian_word_router,
    confirm_stage_router,
)
