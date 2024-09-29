from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
# from .others import get_kb_yes_no

from db import query


# == InlineKeyboard ================================================================================
def get_kb_admin(user_id, chat_id):
    return InlineKeyboardBuilder().add(
        InlineKeyboardButton(
            text="Показать мой ID",
            callback_data=f"adm_get_my_id:{user_id}"
        ),
        InlineKeyboardButton(
            text="Показать ID чата",
            callback_data=f"adm_get_chat_id:{chat_id}"
        ),
        InlineKeyboardButton(
            text="Пользователи бота",
            callback_data="adm_get_users"
        ),
    ).adjust(1).as_markup()


async def get_kb_admin_users():
    users = await query.get_users()

    kb = InlineKeyboardBuilder()

    if users:
        for user in users:
            kb.add(
                InlineKeyboardButton(
                    text=f"{user.full_name}",
                    callback_data=f"adm_get_user:{user.id}:{user.full_name}"
                )
            )

    return kb.adjust(1).as_markup()


def get_kb_admin_user(user_id: str, user_full_name: str):
    return InlineKeyboardBuilder().add(
        InlineKeyboardButton(
            text="🗑️ Удалить",
            callback_data=f"adm_user_delete:{user_id}:{user_full_name}"
        )
    ).adjust(1).as_markup()
