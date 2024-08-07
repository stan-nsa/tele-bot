import os
from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.fsm.context import FSMContext

import config
import keyboards

router = Router(name=__name__)

img_folder = os.path.abspath(config.IMG_FOLDER)


# Состояния для загрузки информации по товару
class FSMSku(StatesGroup):
    name = State()      # Состояние для ввода артикула товара
    photos = State()    # Состояние для загрузки фото товара
    delete = State()    # Состояние для удаления товара


# Класс описывающий структуру данных размера фото товара
class SkuPhotoSize:
    file_id: str    # Идентификатор файла
    width: int      # Ширина фото в пикселях
    height: int     # Высота фото в пикселях

    # Конструктор класса
    def __init__(self,
                 photo_size: types.PhotoSize = None,
                 file_id: str = None, width: int = None, height: int = None):
        if photo_size:
            self.file_id = photo_size.file_id
            self.width = photo_size.width
            self.height = photo_size.height
        else:
            self.file_id = file_id
            self.width = width
            self.height = height


# Класс описывающий структуру данных фото товара
class SkuPhoto:
    name: str                       # Имя файла
    chat_id: int                    # Идентификатор чата
    message_id: int                 # Идентификатор сообщения, содержащего фото
    sizes: list[SkuPhotoSize]       # Список размеров фотографии товара

    # Конструктор класса
    def __init__(self,
                 message: types.Message = None,
                 sizes: list[types.PhotoSize] = None,
                 chat_id: int = None, message_id: int = None, name: str = None):
        self.name = name
        self.sizes = list[SkuPhotoSize]()

        if message:
            self.chat_id = message.chat.id
            self.message_id = message.message_id
            sizes = message.photo
        else:
            self.chat_id = chat_id
            self.message_id = message_id

        if sizes:
            for size in sizes:
                sku_photo_size = SkuPhotoSize(photo_size=size)
                self.sizes.append(sku_photo_size)


# Класс описывающий структуру данных товара
class SkuData:
    id: str                     # Идентификатор
    name: str                   # Артикул
    photos: {int: SkuPhoto}     # Словарь фотографий товара dict(message_id=SkuPhoto)

    # Конструктор класса
    def __init__(self, sku_id: str = None, name: str = None, photos: {int: SkuPhoto} = None):
        self.id = sku_id
        self.name = name
        self.photos = photos if photos is not None else dict()

    # Артикул жирным текстом
    def get_name_text(self):
        name_text = f"<b>{self.name}</b>" if self.name and len(self.name) else ''
        return name_text

    # Часть текста с артикулом жирным текстом
    def get_name_text2(self):
        name_text = f" с артикулом: {self.get_name_text()}" if self.name and len(self.name) else ''
        return name_text

    async def delete_photos_from_chat(self, chat: types.Chat = None):
        if (not len(self.photos)) or (not chat):
            return

        await chat.bot.delete_messages(
            chat.id,
            [p.message_id for p in self.photos.values()]
        )
        self.photos.clear()


# == Добавление товара ============================================================================
# Обработчик комады /add и кнопки "Добавить товар" для запуска машины состояний для добавления товара
@router.message(Command('add', ignore_case=True), StateFilter(default_state))
@router.callback_query(F.data == "sku_add", StateFilter(default_state))
async def handler_sku_add(msg_cbq: types.Message | types.CallbackQuery, state: FSMContext):
    await state.set_state(FSMSku.name)

    data = dict(sku_data=SkuData())
    await state.set_data(data)

    text = "Начинаем добавлять товар.\n\n" \
           "📝 Введите артикул товара:"

    if type(msg_cbq) is types.CallbackQuery:
        await msg_cbq.answer()

        await msg_cbq.message.edit_text(
            text=text,
            reply_markup=keyboards.get_kb_sku_cancel().as_markup()
        )
    else:
        await msg_cbq.answer(
            text=text,
            reply_markup=keyboards.get_kb_sku_cancel().as_markup()
        )
        await msg_cbq.delete()
# =================================================================================================


# == Отмена добавления товара =====================================================================
# Обработчик комады /cancel для остановки машины состояний добавления товара
@router.message(Command('cancel', ignore_case=True), ~StateFilter(default_state))
async def handler_cmd_cancel(message: types.Message, state: FSMContext):
    if await state.get_state() == FSMSku.name:
        await state.clear()

        await message.answer(
            text=f"❌ 📦 Добавление товара отменено!",
            reply_markup=keyboards.get_kb_sku().as_markup()
        )
    else:
        data = await state.get_data()
        sku_data = data['sku_data']

        await message.answer(
            text=f"⁉️ Вы действительно хотите отменить добавление товара{sku_data.get_name_text2()}?",
            reply_markup=keyboards.get_kb_sku_cancel_yes_no().as_markup()
        )
    await message.delete()


# Обработчик кнопки "Отменить добавление товара" для остановки машины состояний добавления товара
@router.callback_query(F.data == "sku_cancel", ~StateFilter(default_state))
async def handler_sku_cancel(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()

    if await state.get_state() == FSMSku.name:
        await state.clear()

        await callback.message.edit_text(
            text=f"❌ 📦 Добавление товара отменено!",
            reply_markup=keyboards.get_kb_sku().as_markup()
        )
    else:
        data = await state.get_data()
        sku_data = data['sku_data']

        await callback.message.answer(
            text=f"⁉️ Вы действительно хотите отменить добавление товара{sku_data.get_name_text2()}?",
            reply_markup=keyboards.get_kb_sku_cancel_yes_no().as_markup()
        )


# Обработчик кнопки "Да" для подтверждения остановки машины состояний добавления товара
@router.callback_query(F.data == "sku_cancel_btn_yes", ~StateFilter(default_state))
async def handler_sku_cancel_yes(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()

    message = callback.message
    data = await state.get_data()
    sku_data = data['sku_data']
    num_photos = len(sku_data.photos)

    await sku_data.delete_photos_from_chat(chat=message.chat)

    await state.clear()

    await message.edit_text(
        text=f"❌ 📦 Добавление товара{sku_data.get_name_text2()} отменено (удалено {num_photos} фото)!",
        reply_markup=keyboards.get_kb_sku().as_markup()
    )


# Обработчик кнопки "Нет" для отмены остановки машины состояний добавления товара
@router.callback_query(F.data == "sku_cancel_btn_no", ~StateFilter(default_state))
async def handler_sku_cancel_no(callback: types.CallbackQuery):
    await callback.answer()

    await callback.message.delete()
# =================================================================================================


# == Артикул товара ===============================================================================
# Обработчик состояния для ввода артикула товара
@router.message(StateFilter(FSMSku.name), F.text)
async def handler_state_name(message: types.Message, state: FSMContext):
    data = await state.get_data()
    sku_data = data['sku_data']
    sku_data.name = message.text.strip()
    await state.set_data(data)

    await state.set_state(FSMSku.photos)

    await message.reply(
        text=f"Артикул товара: {sku_data.get_name_text()}.\n\n"
             f"📸 Сфотографируйте товар!",
        reply_markup=keyboards.get_kb_sku_cancel().as_markup()
    )


# Обработчик состояния для ввода артикула товара, если прислали не текст
@router.message(StateFilter(FSMSku.name), ~F.text)
async def handler_state_name_not_text(message: types.Message):
    await message.reply(
        text=f"Это не артикул!\n\n"
             f"📝 Введите артикул товара:",
        reply_markup=keyboards.get_kb_sku_cancel().as_markup()
    )
# =================================================================================================


# == Фото товара ==================================================================================
# Обработчик состояния для добавдения фото товара
@router.message(StateFilter(FSMSku.photos), F.photo)
async def handler_sku_photos(message: types.Message, state: FSMContext):
    data = await state.get_data()
    sku_data = data['sku_data']

    sku_data.photos[message.message_id] = SkuPhoto(message=message)

    await state.set_data(data)

    await message.reply(
        text=f"✅ 📸 Фото для товара{sku_data.get_name_text2()} получено!\n\n"
             f"📸 Сфотографируйте товар!",
        reply_markup=keyboards.get_kb_sku_photo().as_markup()
    )


# Обработчик состояния для добавдения фото товара, если прислали не фото
@router.message(StateFilter(FSMSku.photos), ~F.photo)
async def handler_sku_photos_not_photo(message: types.Message):
    await message.reply(
        text=f"Это не фото!\n\n"
             f"📸 Сфотографируйте товар!",
        reply_markup=keyboards.get_kb_sku_save_cancel().as_markup()
    )


# Обработчик кнопки "Удалить это фото" для подтверждения остановки машины состояний добавления товара
@router.callback_query(StateFilter(FSMSku.photos), F.data == "sku_photo_delete")
async def handler_sku_photo_delete(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()

    message = callback.message
    data = await state.get_data()
    sku_data = data['sku_data']

    if len(sku_data.photos):
        sku_data.photos.pop(message.reply_to_message.message_id)
        await state.set_data(data)

        await message.reply_to_message.delete()

        await message.edit_text(
            text=f"🗑️ 📸 Это фото для товара{sku_data.get_name_text2()} удалено!\n\n"
                 f"📸 Сфотографируйте товар!",
            reply_markup=keyboards.get_kb_sku_save_cancel().as_markup()
        )
# =================================================================================================


# == Сохранение товара ============================================================================
# Обработчик комады /save и кнопки "Завершить добавление товара"
# для завершения машины состояний добавления товара и сохранения фото товара
@router.message(Command('save', ignore_case=True), StateFilter(FSMSku.photos))
@router.callback_query(F.data == "sku_save", StateFilter(FSMSku.photos))
async def handler_sku_save(msg_cbq: types.Message | types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    sku_data = data['sku_data']

    saved_files_text = ''
    for i, photo in enumerate(sku_data.photos.values(), start=1):
        photo_largest = photo.sizes[-1]
        photo_largest.name = config.IMG_FILE_NAME_TEMPLATE % (
            sku_data.name, i, photo_largest.width, photo_largest.height)
        # photo_largest.name = config.IMG_FILE_NAME_TEMPLATE % (sku_data.name, i)
        await msg_cbq.bot.download(
            file=photo_largest,
            destination=os.path.join(img_folder, photo_largest.name)
        )
        saved_files_text += f"📸️ {photo_largest.name} - разрешение: {photo_largest.width} x {photo_largest.height}\n"

    await state.clear()

    if type(msg_cbq) is types.CallbackQuery:
        await msg_cbq.answer()
        await msg_cbq.message.delete_reply_markup()
        msg_cbq = msg_cbq.message

    await msg_cbq.answer(
        text=f"✅ 📦 Товар{sku_data.get_name_text2()} сохранен!\n\n"
             f"Сохранено {len(sku_data.photos)} фото:\n"
             f"{saved_files_text}",
        reply_markup=keyboards.get_kb_sku().as_markup()
    )
# =================================================================================================


# == Удаление товара ============================================================================
# Обработчик комады /delete и кнопки "Удалить товар" для запуска машины состояний для удаления товара
@router.message(Command('delete', ignore_case=True), StateFilter(default_state))
@router.callback_query(F.data == "sku_delete", StateFilter(default_state))
async def handler_sku_delete(msg_cbq: types.Message | types.CallbackQuery, state: FSMContext):
    await state.set_state(FSMSku.delete)

    data = dict(sku_data=SkuData())
    await state.set_data(data)

    text = "🗑️ Начинаем удалять товар.\n\n" \
           "📝 Введите артикул товара:"

    if type(msg_cbq) is types.CallbackQuery:
        await msg_cbq.answer()

        await msg_cbq.message.edit_text(
            text=text,
            reply_markup=keyboards.get_kb_sku_cancel().as_markup()
        )
    else:
        await msg_cbq.answer(
            text=text,
            reply_markup=keyboards.get_kb_sku_cancel().as_markup()
        )
        await msg_cbq.delete()
# =================================================================================================
