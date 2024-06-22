__all__ = ("router",)

from aiogram import Router

from .default import router as default_router

router = Router(name=__name__)

router.include_routers(
    default_router,
)
