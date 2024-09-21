from aiogram import Router, types, F
from aiogram.filters import Command

from config import config
# from filters import IsAdmin

router = Router(name=__name__)
# Роутер только для лички (фильтры уже прописаны в /handlers/__init__.py)
# router.message.filter(F.chat.type == 'private')
# router.callback_query.filter(F.chat.type == 'private')


# @router.message(Command('admin', ignore_case=True), IsAdmin(config.bot.admins))
@router.message(Command('admin', ignore_case=True), F.from_user.id.in_(config.bot.admins))
async def handler_command_admin(message: types.Message):
    await message.answer(
        text=f"Привет, Админ! 😍")


@router.message(Command('admin', ignore_case=True))
async def handler_command_admin(message: types.Message):
    await message.answer(
        text=f"А ты точно Админ? 😏")
