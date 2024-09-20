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
# ⚠️ - https://emojis.wiki/ru/preduprezhdenie/


from aiogram.types import InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from .others import get_kb_yes_no

# == InlineKeyboar ================================================================================
sku_kb_buttons = dict(
    add=InlineKeyboardButton(text="📦 Добавить товар", callback_data="sku_add"),
    cancel=InlineKeyboardButton(text="❌ Отменить добавление товара", callback_data="sku_cancel"),
    save=InlineKeyboardButton(text="📦 Завершить добавление товара", callback_data="sku_save"),
    photo_delete=InlineKeyboardButton(text="🗑️ Удалить это фото", callback_data="sku_photo_delete"),
    delete=InlineKeyboardButton(text="🗑️ Удалить товар", callback_data="sku_delete"),
    delete_cancel=InlineKeyboardButton(text="❌ Отменить удаление товара", callback_data="sku_delete_cancel"),
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


def get_kb_sku_cancel():
    return get_kb_sku_builder(buttons=['cancel'])


def get_kb_sku_photo():
    return get_kb_sku_builder(
        buttons=[
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


def get_kb_sku_delete_cancel():
    return get_kb_sku_builder(buttons=['delete_cancel'])


def get_kb_sku_delete_yes_no():
    return get_kb_yes_no(prefix="sku_delete_")


# == ReplyKeyboard ================================================================================
def get_kb_sku_fsm():
    kb = ReplyKeyboardBuilder()
    kb.row(
        KeyboardButton(text='Завершить'),
        KeyboardButton(text='Отменить')
    )
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)
