from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from config import USERS


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:

        # ...
        # Здесь выполняется код на входе в middleware
        # ...

        if event.event.from_user.id in USERS:
            result = await handler(event, data)
        else:
            result = None

        # ...
        # Здесь выполняется код на выходе из middleware
        # ...

        return result
