__all__ = ("router",)

from aiogram import Router

from .start_update import router as start_update_router
from .update_en import router as update_en_router
from .update_ru import router as update_ru_router
from .confirm import router as confirm_router

router = Router(name=__name__)

router.include_routers(
    start_update_router,
    update_en_router,
    update_ru_router,
    confirm_router
)

