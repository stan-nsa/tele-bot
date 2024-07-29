# 📸 - https://emojis.wiki/ru/fotokamera-so-vspyshkoj/
# ⁉️ - https://emojis.wiki/ru/vosklicatelnyj-i-voprositelnyj-znaki-krasnogo-cveta/
# 📝 - https://emojis.wiki/ru/pamyatka/
# ✅ - https://emojis.wiki/ru/zelenaya-galochka/
# ✔️ - https://emojis.wiki/ru/galochka/
# ❌ - https://emojis.wiki/ru/znachok-kresta/


import os
from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.fsm.context import FSMContext

import keyboards


router = Router(name=__name__)


IMG_FOLDER = 'd:/Projects/tele-bot/img'
IMG_FILE_NAME_TEMPLATE = '%s-%d.jpg'
img_folder = os.path.abspath(IMG_FOLDER)


# Состояния для загрузки информации по товару
class FSMSku(StatesGroup):
    name = State()      # Состояние для ввода артикула товара
    photos = State()    # Состояние для загрузки фото товара


# Обработчик комады /sku для запуска машины состояний для добавления товара
@router.message(Command('sku', ignore_case=True), StateFilter(default_state))
async def handler_cmd_sku(message: types.Message, state: FSMContext):
    await state.set_state(FSMSku.name)

    await message.answer(
        text=f"Начинаем добавлять товар.\n\n"
             f"📝 Введите артикул товара:"
    )
    await message.delete()


# Обработчик кнопки "Добавить товар" для запуска машины состояний для добавления товара
@router.callback_query(F.data == "sku_add", StateFilter(default_state))
async def handler_sku_add(callback: types.CallbackQuery, state: FSMContext):
    await handler_cmd_sku(callback.message, state)
    await callback.answer()


# Обработчик состояния для ввода артикула товара
@router.message(StateFilter(FSMSku.name))
async def handler_state_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)

    await message.reply(
        text=f"Вы ввели артикул товара: <b>{message.text}</b>.\n\n"
             f"⁉️ Всё верно?",
        reply_markup=keyboards.get_kb_sku_name()
    )


# Обработчик кнопки "Верно" состояния для ввода артикула товара
@router.callback_query(F.data == "sku_name_ok", StateFilter(FSMSku.name))
async def handler_sku_name_ok(callback: types.CallbackQuery, state: FSMContext):
    message = callback.message
    data = await state.get_data()
    sku = data.get('name')

    await state.set_state(FSMSku.photos)

    await message.answer(
        text=f"Артикул товара: <b>{sku}</b>.\n\n"
             f"📸 Сфотографируйте товар:"
    )
    await message.delete()
    await callback.answer()


# Обработчик кнопки "Верно" состояния для ввода артикула товара
@router.callback_query(F.data == "sku_name_edit", StateFilter(FSMSku.name))
async def handler_sku_name_edit(callback: types.CallbackQuery, state: FSMContext):
    message = callback.message
    await handler_cmd_sku(message, state)
    await callback.answer()


# Обработчик состояния для добавдения фото товара
@router.message(StateFilter(FSMSku.photos), F.photo)
async def handler_sku_photos(message: types.Message, state: FSMContext):
    data = await state.get_data()
    sku = data.get('name')
    photos = data.get('photos')

    if photos is None:
        photos = list()

    photos.append(message.photo[-1].file_id)
    await state.update_data(photos=photos)

    await message.reply(
        text=f"✅ Фото для товара с артикулом: <b>{sku}</b> получено!"
    )


# Обработчик комады /save для завершения машины состояний добавления товара и сохранения фото товара
@router.message(Command('save', ignore_case=True), StateFilter(FSMSku.photos))
async def handler_sku_save(message: types.Message, state: FSMContext):
    data = await state.get_data()
    sku = data.get('name')
    photos = data.get('photos')

    for i, photo in enumerate(photos, start=1):
        await message.bot.download(
            file=photo,
            destination=os.path.join(img_folder, IMG_FILE_NAME_TEMPLATE % (sku, i))
        )

    await state.clear()

    await message.answer(
        text=f"✅ Товар с артикулом: <b>{sku}</b> сохранен!"
    )
    await message.delete()


# Обработчик состояния для добавдения фото товара, если прислали не фото
@router.message(StateFilter(FSMSku.photos), ~F.photo)
async def handler_sku_photos_not_photo(message: types.Message):
    await message.reply(
        text=f"Это не фото!\n\n"
             f"📸 Сфотографируйте товар:"
    )


# Обработчик комады /cancel для остановки машины состояний добавления товара
@router.message(Command('cancel', ignore_case=True), ~StateFilter(default_state))
async def handler_cmd_sku_cancel(message: types.Message, state: FSMContext):
    data = await state.get_data()
    sku = data.get('name')

    await message.answer(
        text=f"⁉️ Вы действительно хотите отменить добавление товара с артикулом: <b>{sku}</b>?",
        reply_markup=keyboards.get_kb_sku_cancel()
    )
    await message.delete()


# Обработчик кнопки "Отменить" для остановки машины состояний добавления товара
@router.callback_query(F.data == "sku_cancel", ~StateFilter(default_state))
async def handler_sku_cancel(callback: types.CallbackQuery, state: FSMContext):
    await handler_cmd_sku_cancel(callback.message, state)
    await callback.answer()


# Обработчик кнопки "Да" для подтверждения остановки машины состояний добавления товара
@router.callback_query(F.data == "sku_cancel_btn_yes", ~StateFilter(default_state))
async def handler_sku_cancel_yes(callback: types.CallbackQuery, state: FSMContext):
    message = callback.message
    data = await state.get_data()
    sku = data.get('name')

    await state.clear()

    await message.answer(
        text=f"❌ Добавление товара с артикулом: <b>{sku}</b> отменено!"
    )
    await message.delete()
    await callback.answer()


# Обработчик кнопки "Нет" для отмены остановки машины состояний добавления товара
@router.callback_query(F.data == "sku_cancel_btn_no", ~StateFilter(default_state))
async def handler_sku_cancel_no(callback: types.CallbackQuery, state: FSMContext):
    await handler_sku_name_ok(callback, state)
    await callback.answer()
