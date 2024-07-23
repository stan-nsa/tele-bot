import asyncio
import logging
# import sys
from environs import Env

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from handlers import router as handlers_router

env = Env()
env.read_env()


async def main():
    dp = Dispatcher()
    dp.include_router(handlers_router)

    bot = Bot(token=env('BOT_TOKEN'),
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)  # , stream=sys.stdout)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Stop Tele-Bot')
