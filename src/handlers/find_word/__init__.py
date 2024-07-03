__all__ = ("router",)

from aiogram import Router

from .exit import router as exit_router
from .get_word import router as get_word_router
from .request_processing import router as request_processing_router
from .update_word import router as update_word_router

router = Router(name=__name__)

router.include_routers(
    exit_router, update_word_router, get_word_router, request_processing_router
)
