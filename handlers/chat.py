# в ботфазере даем боту возможность читать все сообщения (Group Privacy)

from aiogram import Router, types
from aiogram.filters import IS_MEMBER, IS_NOT_MEMBER, ChatMemberUpdatedFilter
from db.query import get_user, add_user, delete_user


router = Router(name=__name__)


# Исключение участника из группы
@router.chat_member(ChatMemberUpdatedFilter(IS_MEMBER >> IS_NOT_MEMBER))
async def on_user_leave(event: types.ChatMemberUpdated):
    user = event.new_chat_member.user
    if await get_user(user):
        await delete_user(user)


# Добавление участника в группу
@router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def on_user_join(event: types.ChatMemberUpdated):
    user = event.new_chat_member.user
    if not await get_user(user):
        await add_user(user)
