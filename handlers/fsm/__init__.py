from aiogram import Router
from .sku import router as sku_roter


router = Router()
router.include_router(sku_roter)
