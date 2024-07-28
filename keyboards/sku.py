from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_kb_sku_name():
    kb_sku_name = InlineKeyboardBuilder()
    kb_sku_name.add(

            InlineKeyboardButton(text="Верно", callback_data="sku_name_ok"),
            InlineKeyboardButton(text="Отмена", callback_data="sku_name_cancel"),

    )

    kb_sku_name.adjust(2)

    return kb_sku_name.as_markup()
