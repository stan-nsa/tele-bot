from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from config import USERS, ADMIN


class UserMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]
                       ) -> Any:

        # if ((not USERS) or (event.event.from_user.id in USERS)) or \
        #         ((not ADMIN) or (event.event.from_user.id == ADMIN)):
        if (not USERS) or (event.event.from_user.id in USERS):
            result = await handler(event, data)
        else:
            result = None

        return result
