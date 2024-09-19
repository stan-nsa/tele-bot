from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command
import keyboards
from help import help_text

router = Router(name=__name__)
# Роутер только для лички (фильтры уже прописаны в /handlers/__init__.py)
# router.message.filter(F.chat.type == 'private')
# router.callback_query.filter(F.chat.type == 'private')


# == Обработчик команды /start ====================================================================
@router.message(CommandStart(ignore_case=True))
async def handler_command_start(message: types.Message):
    await message.answer(
        text="""
Это бот для сбора фотографий товаров!

Для начала работы нажмите <b>"Добавить товар"</b>

Чтобы узнать, как пользоваться ботом нажмите <b>"Помощь"</b>""",
        reply_markup=(keyboards.sku.get_kb_sku().attach(keyboards.get_kb_help())).as_markup()
    )
    await message.delete()
# =================================================================================================


# == Обработчик команды /help и кнопки "Помощь" ===================================================
@router.message(Command('help', ignore_case=True))
@router.callback_query(F.data == "help")
async def handler_command_help(msg_cbq: types.Message | types.CallbackQuery):
    if type(msg_cbq) is types.CallbackQuery:
        await msg_cbq.answer()
        await msg_cbq.message.edit_text(
            text=help_text,
            reply_markup=keyboards.get_kb_sku().as_markup()
        )
    else:
        await msg_cbq.answer(
            text=help_text,
            reply_markup=keyboards.get_kb_sku().as_markup()
        )
        await msg_cbq.delete()
# =================================================================================================
