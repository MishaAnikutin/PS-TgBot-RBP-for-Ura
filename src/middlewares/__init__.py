from aiogram import Router
from .printer_middleware import CheckCartridgeMiddleware, CheckPagesMiddleware


__all__ = ["CheckCartridgeMiddleware", "CheckPagesMiddleware"]

