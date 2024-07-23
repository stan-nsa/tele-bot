from aiogram import Router, types
from aiogram.filters import CommandStart, Command


router = Router(name=__name__)


@router.message(CommandStart())
async def handler_command_start(message: types.Message):
    await message.answer(
        text=f"Привет!\n"
             f"<b>Погнали!!!</b>")


@router.message(Command('help'))
async def handler_command_help(message: types.Message):
    await message.answer(
        text=f"Чем помочь?")
