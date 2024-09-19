from aiogram import Router, F
from .commands import router as commands_router
from .fsm import router as fsm_router
from .echo import router as echo_router
from .chat import router as chat_router


router = Router(name=__name__)
# Роутер только для лички (фильтры для всех подключенных роутеров!!!) - уже прописаны в main.py
# router.message.filter(F.chat.type == 'private')
# router.callback_query.filter(F.message.chat.type == 'private')


router.include_router(commands_router)
router.include_router(fsm_router)
router.include_router(chat_router)

# Эхо-роутер должен быть самым последним в списке подключения роутеров
# router.include_router(echo_router)
