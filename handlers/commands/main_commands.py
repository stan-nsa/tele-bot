from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command, or_f
import keyboards
from help import help_text

router = Router(name=__name__)
# Роутер только для лички (фильтры уже прописаны в /handlers/__init__.py)
# router.message.filter(F.chat.type == 'private')
# router.callback_query.filter(F.chat.type == 'private')


# == Обработчик команды /start ====================================================================
@router.message(or_f(
    CommandStart(ignore_case=True),
    F.text.lower().contains('старт'),
    F.text.lower().contains('запуск'))
)
async def handler_command_start(message: types.Message):
    await message.answer(
        text="""
Это бот для сбора фотографий товаров!

Для начала работы нажмите <b>"Добавить товар"</b>

Чтобы узнать, как пользоваться ботом нажмите <b>"Помощь"</b>""",
        reply_markup=keyboards.get_kb_sku_start()
    )
    await message.delete()
# =================================================================================================


# == Обработчик команды /help и кнопки "Помощь" ===================================================
@router.message(or_f(Command('help', ignore_case=True), F.text.lower().contains('помощь')))
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
            reply_markup=keyboards.get_kb_sku_start()
        )
        await msg_cbq.delete()
# =================================================================================================
