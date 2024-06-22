__all__ = ("router",)

from aiogram import Router

from .admin import router as admin_router
from .default import router as default_router


router = Router(name=__name__)

router.include_routers(
    admin_router,
    default_router,
)
