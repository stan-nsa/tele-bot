from aiogram import Router, types
from aiogram.filters import CommandStart, Command
import keyboards

router = Router(name=__name__)


@router.message(CommandStart(ignore_case=True))
async def handler_command_start(message: types.Message):
    await message.answer(
        text=f"Привет!\n"
             f"<b>Погнали!!!</b>",
        reply_markup=keyboards.sku.get_kb_sku()
    )


@router.message(Command('help', ignore_case=True))
async def handler_command_help(message: types.Message):
    await message.answer(
        text=f"Чем помочь?")
