from aiogram import Router, types
from aiogram.filters import Command


router = Router(name=__name__)


@router.message(Command('admin'))
async def handler_command_help(message: types.Message):
    await message.answer(
        text=f"А ты Админ?")
