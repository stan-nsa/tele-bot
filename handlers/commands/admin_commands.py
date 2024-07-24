import os
from aiogram import Router, types, F
from aiogram.filters import Command


router = Router(name=__name__)


IMG_FOLDER = 'd:/Projects/tele-bot/img'
IMG_FILE_NAME = 'img-%d.jpg'
img_folder = os.path.abspath(IMG_FOLDER)


@router.message(Command('admin', ignore_case=True))
async def handler_command_help(message: types.Message):
    await message.answer(
        text=f"А ты Админ?")


@router.message(F.photo)
async def get_photo(message: types.Message):
    #await message.bot.download(file=p.file_id, destination=os.path.join(img_folder, IMG_FILE_NAME % 0))
    for i, p in enumerate(message.photo):
        await message.bot.download(file=p.file_id, destination=os.path.join(img_folder, IMG_FILE_NAME % i))
