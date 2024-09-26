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


# == InlineKeyboard ================================================================================
def get_kb_sku_photo_delete():
    return InlineKeyboardBuilder().add(
        InlineKeyboardButton(
            text="🗑️ Удалить это фото",
            callback_data="sku_photo_delete"
        )
    )


def get_kb_sku_cancel_yes_no():
    return get_kb_yes_no(prefix="sku_cancel_")


def get_kb_sku_delete_yes_no():
    return get_kb_yes_no(prefix="sku_delete_")


# == ReplyKeyboard ================================================================================
def get_kb_sku_start():
    kb = ReplyKeyboardBuilder()
    kb.row(
        KeyboardButton(text="📦 Добавить товар"),
        KeyboardButton(text="❓ Помощь")
    )
    return kb.as_markup(resize_keyboard=True)  # , one_time_keyboard=True, )


def get_kb_sku_fsm(input_field_placeholder: str = None):
    kb = ReplyKeyboardBuilder()
    kb.row(
        KeyboardButton(text="📦 Завершить"),
        KeyboardButton(text="❌ Отменить")
    )
    return kb.as_markup(resize_keyboard=True, input_field_placeholder=input_field_placeholder)


def get_kb_sku_delete():
    kb = ReplyKeyboardBuilder()
    kb.row(
        KeyboardButton(text="❌ Отменить удаление товара")
    )
    return kb.as_markup(resize_keyboard=True, input_field_placeholder="Введите артикул товара")
