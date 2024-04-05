from .user_handlers import user_router
from aiogram import Router

from ..middlewares import CheckPagesMiddleware, CheckCartridgeMiddleware

router = Router()
router.include_routers(user_router)
router.message.middleware(CheckPagesMiddleware())
router.message.middleware(CheckCartridgeMiddleware())

__all__ = ['router']
