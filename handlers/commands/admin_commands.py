from aiogram import Router, types
from aiogram.filters import Command


router = Router(name=__name__)


@router.message(Command('admin', ignore_case=True))
async def handler_command_admin(message: types.Message):
    await message.answer(
        text=f"А ты Админ?")
