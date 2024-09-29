from aiogram import Bot, Router, types, F
from aiogram.filters import Command
import keyboards.admin as kb_admin
from keyboards import get_kb_yes_no

from config import config

from db import query

# from filters import IsAdmin

router = Router(name=__name__)


# Роутер только для лички (фильтры уже прописаны в /handlers/__init__.py)
# router.message.filter(F.chat.type == 'private')
# router.callback_query.filter(F.chat.type == 'private')


# @router.message(Command('admin', ignore_case=True), IsAdmin(config.bot.admins))
@router.message(Command('admin', ignore_case=True), F.from_user.id.in_(config.bot.admins))
async def handler_command_admin(message: types.Message, bot: Bot):
    await message.delete()

    await bot.send_message(
        chat_id=message.from_user.id,
        text=f"Привет, Админ! 😍",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await bot.send_message(
        chat_id=message.from_user.id,
        text="Админка",
        reply_markup=kb_admin.get_kb_admin(
            user_id=message.from_user.id,
            chat_id=message.chat.id
        )
    )


@router.message(Command('admin', ignore_case=True))
async def handler_command_admin(message: types.Message):
    if not config.bot.admins:
        await message.answer(
            text="Список админов не настроен!\n\n"
                 "Узнайте свой ID, пропишите его в конфигурационном файле бота и перезапустите бота!",
            reply_markup=kb_admin.get_kb_admin(
                user_id=message.from_user.id,
                chat_id=message.chat.id
            )
        )
    else:
        await message.answer(
            text="А ты точно Админ? 😏")


@router.callback_query(F.data == "adm_get_users")
async def handler_adm_get_users(callback: types.CallbackQuery):
    await callback.answer()

    await callback.message.edit_text(
        text="Пользователи бота:",
        reply_markup=await kb_admin.get_kb_admin_users()
    )


@router.callback_query(F.data.startswith("adm_get_user:"))
async def handler_adm_get_user(callback: types.CallbackQuery):
    await callback.answer()

    cmd_str, id_str, full_name_str = callback.data.split(":")

    await callback.message.answer(
        text="Пользователь бота:\n"
             f"<b>{full_name_str}</b>",
        reply_markup=kb_admin.get_kb_admin_user(user_id=id_str, user_full_name=full_name_str)
    )


@router.callback_query(F.data.startswith("adm_user_delete:"))
async def handler_adm_user_delete(callback: types.CallbackQuery):
    await callback.answer()

    cmd_str, id_str, full_name_str = callback.data.split(":")

    await callback.message.edit_text(
        text="🗑️ Удалить пользователя бота:\n"
             f"<b>{full_name_str}</b>?",
        reply_markup=get_kb_yes_no(prefix=f"adm_del_user:{id_str}:{full_name_str}:").as_markup()
    )


@router.callback_query(F.data.startswith("adm_del_user:"))
async def handler_adm_delete_user(callback: types.CallbackQuery):
    await callback.answer()

    cmd_str, id_str, full_name_str, btn_str = callback.data.split(":")

    if btn_str == "btn_yes":
        await query.delete_user_by_id(user_id=id_str)

        await callback.message.edit_text(
            text="Пользователь бота:\n"
                 f"<b>{full_name_str}</b>\n"
                 "🗑️ Удален!",
            reply_markup=None
        )
    else:
        await callback.message.edit_text(
            text="🗑️ Удаление пользователя бота:\n"
                 f"<b>{full_name_str}</b>\n"
                 "Отменено!",
            reply_markup=None
        )


@router.callback_query(F.data.startswith("adm_get_"))
async def handler_adm_get_my_id(callback: types.CallbackQuery):
    await callback.answer()

    cmd_str, id_str = callback.data.split(":")

    if cmd_str == "adm_get_my_id":  # Показать ID юзера
        text = f"Ваш ID:\n{id_str}"
    elif cmd_str == "adm_get_chat_id":  # Показать ID чата
        if callback.message.chat.id == int(id_str):  # Предупреждение, если админка была зупущена в личке с ботом
            text = "Вы вызвали админку не в общем чате, а в личке с ботом!\n\n" \
                   "Вызовите админку командой /admin в общем чате, где этот бот добавлен админом!"
        else:  # Показать ID чата
            text = f"ID чата, в котором вы вызвали админку:\n{id_str}"
    else:
        text = "Чего надо?"

    await callback.message.edit_text(
        text=text,
        reply_markup=callback.message.reply_markup
    )
