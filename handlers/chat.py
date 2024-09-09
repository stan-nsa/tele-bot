# в ботфазере даем боту возможность читать все сообщения (Group Privacy)

from aiogram import Router, types
from aiogram.filters import IS_MEMBER, IS_NOT_MEMBER, ChatMemberUpdatedFilter
from db.query import get_user, add_user, update_user, delete_user

from keyboards import get_kb_goto_bot


router = Router(name=__name__)


# Исключение участника из группы
@router.chat_member(ChatMemberUpdatedFilter(IS_MEMBER >> IS_NOT_MEMBER))
async def on_user_leave(event: types.ChatMemberUpdated):
    user = event.new_chat_member.user
    if await get_user(user, 'member'):
        # await delete_user(user)
        await update_user(user, 'not member')


# Добавление участника в группу
@router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def on_user_join(event: types.ChatMemberUpdated):
    user = event.new_chat_member.user
    if await get_user(user):
        await update_user(user, 'member')
    else:
        await add_user(user)

    await event.answer(
        text=f"Добро пожаловать, {user.full_name}!\n\nНажми <b>\"Перейти к боту\"</b>",
        reply_markup=get_kb_goto_bot().as_markup()
    )
