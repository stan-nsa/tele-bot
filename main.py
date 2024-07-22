import asyncio
import logging
#import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from environs import Env

env = Env()
env.read_env()

async def main():
    dp = Dispatcher()
    bot = Bot(token=env('BOT_TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)#, stream=sys.stdout)
    asyncio.run(main())
