# 📸 - https://emojis.wiki/ru/fotokamera-so-vspyshkoj/
# 🎞️ - https://emojis.wiki/ru/kinokadry/
# ⁉️ - https://emojis.wiki/ru/vosklicatelnyj-i-voprositelnyj-znaki-krasnogo-cveta/
# ❓ - https://emojis.wiki/ru/voprositelnyj-znak-krasnogo-cveta/
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

sku_kb_buttons = dict(
    add=InlineKeyboardButton(text="📦 Добавить товар", callback_data="sku_add"),
    cancel=InlineKeyboardButton(text="❌ Отменить добавление товара", callback_data="sku_cancel"),
    save=InlineKeyboardButton(text="📦 Завершить добавление товара", callback_data="sku_save"),
    photo_add=InlineKeyboardButton(text="📸 Добавить ещё фото товара", callback_data="sku_photo_add"),
    photo_delete=InlineKeyboardButton(text="🗑️ Удалить это фото", callback_data="sku_photo_delete"),

)


def get_kb_sku_builder(buttons: list[str], adjust: list[int] | int = 1):
    kb = InlineKeyboardBuilder()
    for btn in buttons:
        kb.add(sku_kb_buttons.get(btn))

    if adjust:
        if type(adjust) is list:
            kb.adjust(*adjust)
        elif type(adjust) is int:
            kb.adjust(adjust)

    return kb


def get_kb_sku():
    return get_kb_sku_builder(buttons=['add'])


def get_kb_sku_name():
    kb = InlineKeyboardBuilder()
    kb.add(
        InlineKeyboardButton(text="✅ Верно", callback_data="sku_name_ok"),
        InlineKeyboardButton(text="📝 Изменить артикул", callback_data="sku_name_edit"),
        sku_kb_buttons.get('cancel'),
    )
    kb.adjust(1)
    return kb


def get_kb_sku_cancel():
    return get_kb_sku_builder(buttons=['cancel'])


def get_kb_sku_photo():
    return get_kb_sku_builder(
        buttons=[
            'photo_add',
            'save',
            'photo_delete',
            'cancel',
        ]
    )


def get_kb_sku_save_cancel():
    return get_kb_sku_builder(
        buttons=[
            'save',
            'cancel',
        ]
    )


def get_kb_sku_cancel_yes_no():
    return get_kb_yes_no(prefix="sku_cancel_")
