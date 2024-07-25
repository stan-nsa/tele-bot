import os
from aiogram import Router, types, F
from aiogram.filters import Command, CommandObject


router = Router(name=__name__)


IMG_FOLDER = 'd:/Projects/tele-bot/img'
IMG_FILE_NAME_TEMPLATE = '%s-%d.jpg'
img_folder = os.path.abspath(IMG_FOLDER)
sku = 'sku'
i = 0


@router.message(Command('admin', ignore_case=True))
async def handler_command_admin(message: types.Message):
    await message.answer(
        text=f"А ты Админ?")


@router.message(Command('sku', ignore_case=True))
async def handler_command_sku(msg: types.Message, command: CommandObject):
    global sku
    sku = command.args

    await msg.reply(
        text=f"Начинаем добавлять товар.\n\n"
             f"Введи артикул товара:")


@router.message(Command('sku_photo', ignore_case=True))
async def handler_command_sku_photo(message: types.Message):
    await message.reply(
        text=f"Сфотографируй товар:")


@router.message(F.photo)
async def get_photo(message: types.Message):
    global i

    await message.bot.download(
        file=message.photo[-1].file_id,
        destination=os.path.join(img_folder, IMG_FILE_NAME_TEMPLATE % (sku, i)))
    # for i, p in enumerate(message.photo):
    #     await message.bot.download(
    #         file=p.file_id,
    #         destination=os.path.join(img_folder, IMG_FILE_NAME_TEMPLATE % (sku, i)))
