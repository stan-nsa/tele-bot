import asyncio
import logging
# import sys 2

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, or_f, and_f
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommandScopeDefault, BotCommandScopeAllPrivateChats
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import router as handlers_router
from handlers.commands.commands_menu import commands_menu

from middlewares import UserMiddleware

from config import config

from db.engine import create_db


async def on_startup():
    print('Start Tele-Bot')
    await create_db()


async def on_shutdown():
    print('Stop Tele-Bot')


async def main():
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(handlers_router)

    # -- Фильтры для всех подключенных роутеров!!!) -----------------
    dp.message.filter(  # Фильтр: пропускать только сообщения в личке или только от админов
        or_f(
            F.chat.type == 'private',
            and_f(
                Command('admin', ignore_case=True),
                F.from_user.id.in_(config.bot.admins)
            )
        )
    )
    dp.callback_query.filter(F.message.chat.type == 'private')
    # ---------------------------------------------------------------

    dp.startup.register(on_startup)
    dp.shutdown.register(on_startup)

    dp.update.outer_middleware(middleware=UserMiddleware())

    bot = Bot(token=config.bot.token,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # Удаляем меню команд в групповых чатах
    await bot.delete_my_commands(scope=BotCommandScopeDefault())

    # Прописываем меню команд для приватного чата с ботом
    await bot.set_my_commands(commands=commands_menu, scope=BotCommandScopeAllPrivateChats())

    # Удаляем неполученные/необработанные обновления/сообщения
    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        # stream=sys.stdout,
    )

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Stop Tele-Bot')
