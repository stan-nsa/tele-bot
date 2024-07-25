from aiogram import Router, types
# from html import escape


router = Router(name=__name__)


@router.message()
async def handler_echo(message: types.Message):
    await message.send_copy(chat_id=message.chat.id)
    # await message.answer(text=escape(message.text))
    # await message.answer(text=message.text)
