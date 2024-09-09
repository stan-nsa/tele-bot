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
    kb = InlineKeyboardBuilder()
    kb.add(
        InlineKeyboardButton(text="✔️ Да", callback_data=f"{prefix}btn_yes"),
        InlineKeyboardButton(text="❌ Нет", callback_data=f"{prefix}btn_no"),
    )
    kb.adjust(2)
    return kb


def get_kb_help():
    kb = InlineKeyboardBuilder()
    kb.add(
        InlineKeyboardButton(text="❓ Помощь", callback_data="help"),
    )
    return kb


def get_kb_goto_bot():
    kb = InlineKeyboardBuilder()
    kb.add(
        InlineKeyboardButton(text="👉 Перейти к боту", url='https://t.me/nsa_tele_bot'),
    )
    return kb
