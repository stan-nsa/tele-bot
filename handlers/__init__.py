from aiogram import Router
from .commands import router as commands_router
from .echo import router as echo_router


router = Router(name=__name__)

router.include_routers(commands_router)

# Эхо-роутер должен быть самым последним в списке подключения роутеров
router.include_routers(echo_router)
