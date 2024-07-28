import os
from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.fsm.context import FSMContext

from keyboards import get_kb_sku_name


router = Router(name=__name__)


IMG_FOLDER = 'd:/Projects/tele-bot/img'
IMG_FILE_NAME_TEMPLATE = '%s-%d.jpg'
img_folder = os.path.abspath(IMG_FOLDER)


# Состояния для загрузки информации по товару
class FSMSku(StatesGroup):
    name = State()      # Состояние для ввода артикула товара
    photos = State()    # Состояние для загрузки фото товара


# Обработчик комады /sku запуска машины состояний для добавления товара
@router.message(Command('sku', ignore_case=True), StateFilter(default_state))
async def handler_command_sku(message: types.Message, state: FSMContext):
    await state.set_state(FSMSku.name)

    await message.reply(
        text=f"Начинаем добавлять товар.\n\n"
             f"Введите артикул товара:"
    )


# Обработчик состояния для ввода артикула товара
@router.callback_query(StateFilter(FSMSku.name), F.data == "sku_name_ok")
async def sku_name(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(FSMSku.photos)

    await callback.message.reply(
        text=f"Артикул товара: <b>{callback.message.text}</b>.\n\n"
             f"Сфотографируй товар:"
    )

@router.message(StateFilter(FSMSku.name))
async def handler_sku_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    # await state.set_state(FSMSku.photos)

    await message.reply(
        text=f"Вы ввели артикул товара: <b>{message.text}</b>.\n\n"
             f"Всё верно?",
        reply_markup=get_kb_sku_name()
    )


# Обработчик состояния для добавдения фото товара
@router.message(StateFilter(FSMSku.photos), F.photo)
async def handler_sku_photos(message: types.Message, state: FSMContext):
    data = await state.get_data()
    photos = data.get('photos')

    if photos is None:
        photos = list()

    photos.append(message.photo[-1].file_id)
    await state.update_data(photos=photos)

    await message.reply(
        text=f"Фото получено"
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

    await message.reply(
        text=f"Товар: <b>{sku}</b> сохранен!"
    )


# Обработчик комады /cancel для остановки машины состояний добавления товара
@router.message(Command('cancel', ignore_case=True), ~StateFilter(default_state))
async def handler_sku_cancel(message: types.Message, state: FSMContext):
    data = await state.get_data()
    sku = data.get('name')

    await state.clear()

    await message.reply(
        text=f"Добавление товара: <b>{sku}</b> отменено!"
    )
