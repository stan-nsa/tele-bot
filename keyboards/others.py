# 📸 - https://emojis.wiki/ru/fotokamera-so-vspyshkoj/
# ⁉️ - https://emojis.wiki/ru/vosklicatelnyj-i-voprositelnyj-znaki-krasnogo-cveta/
# 📝 - https://emojis.wiki/ru/pamyatka/
# ✅ - https://emojis.wiki/ru/zelenaya-galochka/
# ✔️ - https://emojis.wiki/ru/galochka/
# ❌ - https://emojis.wiki/ru/znachok-kresta/
# ➕ - https://emojis.wiki/ru/znak-plyusa/
# 🏷️ - https://emojis.wiki/ru/birka/
# 📦 - https://emojis.wiki/ru/posylka/

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_kb_yes_no(prefix=''):
    kb = InlineKeyboardBuilder()
    kb.add(
        InlineKeyboardButton(text="✔️ Да", callback_data=f"{prefix}btn_yes"),
        InlineKeyboardButton(text="❌ Нет", callback_data=f"{prefix}btn_no"),
    )
    kb.adjust(2)
    return kb.as_markup()
