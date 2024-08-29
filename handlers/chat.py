# в ботфазере даем боту возможность читать все сообщения (Group Privacy)

from aiogram import Router, types
from aiogram.filters import IS_MEMBER, IS_NOT_MEMBER, ChatMemberUpdatedFilter

from config import config


router = Router(name=__name__)


# Исключение участника из группы
@router.chat_member(ChatMemberUpdatedFilter(IS_MEMBER >> IS_NOT_MEMBER))
async def on_user_leave(event: types.ChatMemberUpdated):
    user_id = event.new_chat_member.user.id
    if user_id in config.bot.users:
        config.bot.users.pop(config.bot.users.index(user_id))
        print(config.bot.users)


# Добавление участника в группу
@router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def on_user_join(event: types.ChatMemberUpdated):
    user_id = event.new_chat_member.user.id
    if user_id not in config.bot.users:
        config.bot.users.append(user_id)
        print(config.bot.users)
