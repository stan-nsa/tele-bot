from aiogram import Router
from .main_commands import router as main_commands
from .admin_commands import router as admin_commands


router = Router()
router.include_router(main_commands)
router.include_router(admin_commands)
