from aiogram import Router, F
from aiogram.filters import and_f, or_f

from .sku import router as sku_roter

from config import config


router = Router()
router.include_router(sku_roter)

# Роутер только для лички (фильтры уже прописаны в /handlers/__init__.py)
router.message.filter(
    and_f(
        F.chat.type == 'private',
        or_f(
            lambda demo: config.demo,
            F.from_user.id.in_(config.bot.admins),
        )
    )
)

# router.message.filter(F.chat.type == 'private')
# router.callback_query.filter(F.chat.type == 'private')
