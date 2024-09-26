# 📸 - https://emojis.wiki/ru/fotokamera-so-vspyshkoj/
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


def get_kb_yes_no(prefix: str = ''):
    return InlineKeyboardBuilder().add(
        InlineKeyboardButton(text="✔️ Да", callback_data=f"{prefix}btn_yes"),
        InlineKeyboardButton(text="❌ Нет", callback_data=f"{prefix}btn_no"),
    ).adjust(2)


def get_kb_help():
    return InlineKeyboardBuilder().add(
        InlineKeyboardButton(text="❓ Помощь", callback_data="help"),
    )


def get_kb_goto_bot():
    return InlineKeyboardBuilder().add(
        InlineKeyboardButton(text="👉 Перейти к боту", url='https://t.me/nsa_tele_bot'),
    )
