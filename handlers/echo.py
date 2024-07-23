from aiogram import Router, types


router = Router(name=__name__)


@router.message()
async def handler_command_help(message: types.Message):
    await message.answer(
        text=message.text)
