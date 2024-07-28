from aiogram import Router
from .commands import router as commands_router
from .fsm import router as fsm_router
from .echo import router as echo_router


router = Router(name=__name__)

router.include_router(commands_router)
router.include_router(fsm_router)

# Эхо-роутер должен быть самым последним в списке подключения роутеров
router.include_router(echo_router)
