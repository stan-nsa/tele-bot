from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from config import config
from db.query import get_user


class UserMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]
                       ) -> Any:

        if (event.event.from_user.id in config.bot.admins) or (await get_user(event.event.from_user)):
            result = await handler(event, data)
        else:
            result = None

        return result
