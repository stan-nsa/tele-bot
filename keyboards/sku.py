# 📸 - https://emojis.wiki/ru/fotokamera-so-vspyshkoj/
# ⁉️ - https://emojis.wiki/ru/vosklicatelnyj-i-voprositelnyj-znaki-krasnogo-cveta/
# 📝 - https://emojis.wiki/ru/pamyatka/
# ✅ - https://emojis.wiki/ru/zelenaya-galochka/
# ✔️ - https://emojis.wiki/ru/galochka/
# ❌ - https://emojis.wiki/ru/znachok-kresta/
# ➕ - https://emojis.wiki/ru/znak-plyusa/
# 🏷️ - https://emojis.wiki/ru/birka/
# 📦 - https://emojis.wiki/ru/posylka/
# 🗑️ - https://emojis.wiki/ru/musornaya-korzina/
# 🗳️ - https://emojis.wiki/ru/izbiratelnaya-urna-s-byulletenem/
# 💾 - https://emojis.wiki/ru/disketa/


from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from .others import get_kb_yes_no


def get_kb_sku():
    kb = InlineKeyboardBuilder()
    kb.add(
        InlineKeyboardButton(text="📦 Добавить товар", callback_data="sku_add"),
    )
    kb.adjust(1)
    return kb.as_markup()


def get_kb_sku_name():
    kb = InlineKeyboardBuilder()
    kb.add(
        InlineKeyboardButton(text="✅ Верно", callback_data="sku_name_ok"),
        InlineKeyboardButton(text="📝 Изменить", callback_data="sku_name_edit"),
        InlineKeyboardButton(text="❌ Отменить", callback_data="sku_cancel"),
    )
    kb.adjust(1, 2)
    return kb.as_markup()


def get_kb_sku_photo():
    kb = InlineKeyboardBuilder()
    kb.add(
        InlineKeyboardButton(text="📦 Завершить добавление товара", callback_data="sku_save"),
        InlineKeyboardButton(text="🗑️ Удалить это фото", callback_data="sku_photo_delete"),
        InlineKeyboardButton(text="❌ Отменить добавление товара", callback_data="sku_cancel"),
    )
    kb.adjust(1, 1, 1)
    return kb.as_markup()


def get_kb_sku_cancel():
    return get_kb_yes_no(prefix="sku_cancel_")
