from pathlib import Path
from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter, or_f
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.fsm.context import FSMContext

from config import config
import keyboards
from db.query import add_log


router = Router(name=__name__)
# Роутер только для лички (фильтры уже прописаны в /handlers/__init__.py)
# router.message.filter(F.chat.type == 'private')
# router.callback_query.filter(F.chat.type == 'private')

img_folder = Path(config.img.folder)


# Состояния для загрузки информации по товару
class FSMSku(StatesGroup):
    name = State()  # Состояние для ввода артикула товара
    photos = State()  # Состояние для загрузки фото товара
    delete = State()  # Состояние для удаления товара


# Класс описывающий структуру данных размера фото товара
class SkuPhotoSize:
    file_id: str  # Идентификатор файла
    width: int  # Ширина фото в пикселях
    height: int  # Высота фото в пикселях

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
class SkuPhoto(SkuPhotoSize):
    name: str  # Имя файла
    chat_id: int  # Идентификатор чата
    message_id: int  # Идентификатор сообщения, содержащего фото
    sizes: list[SkuPhotoSize]  # Список размеров фотографии товара

    # Конструктор класса
    def __init__(self,
                 message: types.Message = None,
                 sizes: list[types.PhotoSize] = None,
                 chat_id: int = None, message_id: int = None, name: str = None):
        super().__init__()
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
    id: str  # Идентификатор
    name: str  # Артикул
    photos: dict[int: SkuPhoto]  # Словарь фотографий товара dict(message_id=SkuPhoto)
    store: Path  # Хранилище фотографий
    chat: types.Chat  # Чат

    # Конструктор класса
    def __init__(self,
                 sku_id: str = None,
                 name: str = None,
                 photos: dict[int: SkuPhoto] = None,
                 store: Path = None,
                 chat: types.Chat = None):
        self.id = sku_id
        self.name = name
        self.photos = photos if photos is not None else dict()
        self.store = store
        self.chat = chat

    # Артикул жирным текстом
    def get_name_text(self) -> str:
        name_text = f"<b>{self.name}</b>" if self.name and len(self.name) else ''
        return name_text

    # Часть текста с артикулом жирным текстом
    def get_name_text2(self) -> str:
        name_text = f" с артикулом: {self.get_name_text()}" if self.name and len(self.name) else ''
        return name_text

    # Список файлов фото в хранилище
    def get_files_in_store(self) -> list[Path]:
        files = []
        if len(self.name):
            files = sorted(Path(self.store).glob(f"{self.name}*.jpg"))

        return files

    # Максимальный индекс/номер файла в хранилище
    def get_max_files_index(self) -> int:
        files = self.get_files_in_store()
        idx = 0
        if files:
            idx = int(files[-1].stem.split('_')[1])

        return idx

    # Удаление фото из чата
    async def delete_photos_from_chat(self):
        if len(self.photos):
            await self.chat.bot.delete_messages(
                self.chat.id,
                [p.message_id for p in self.photos.values()]
            )
            self.photos.clear()

    # Удаление фото из хранилища
    def delete_photos_from_store(self) -> list[str]:
        deleted_files = []

        if len(self.name):
            files = self.get_files_in_store()
            for file in files:
                deleted_files.append(file.name)
                file.unlink(missing_ok=True)

            self.photos.clear()

        return deleted_files

    # Сохранение фото в хранилище
    async def save_photos_to_store(self):
        idx = self.get_max_files_index()

        for photo in self.photos.values():
            idx += 1
            photo_largest = photo.sizes[-1]  # Фото с наибольшим разрешением
            for photo_size in photo.sizes:
                # Поиск фото нужного разрешения
                if (photo_size.width <= config.img.resolution) and (photo_size.height <= config.img.resolution):
                    photo_largest = photo_size
                else:
                    break

            photo.file_id = photo_largest.file_id
            photo.width = photo_largest.width
            photo.height = photo_largest.height
            photo.name = config.img.file_name_template % (
                self.name, idx, photo_largest.width, photo_largest.height)
            # photo.name = config.img.file_name_template % (self.name, idx)
            await self.chat.bot.download(
                file=photo.file_id,
                destination=self.store.joinpath(photo.name)
            )


# == Добавление товара ============================================================================
# Обработчик комады /add и кнопки "Добавить товар" для запуска машины состояний для добавления товара
@router.message(
    or_f(
        Command('add', ignore_case=True),
        F.text.lower().contains('добавить')
    ),
    StateFilter(default_state)
)
async def handler_sku_add(message: types.Message, state: FSMContext):
    await state.set_state(FSMSku.name)

    await message.delete()

    data = dict(sku_data=SkuData(store=img_folder, chat=message.chat))
    await state.set_data(data)

    await message.answer(
        text="Начинаем добавлять товар.\n\n"
             "📝 Введите артикул товара:",
        reply_markup=keyboards.get_kb_sku_fsm(input_field_placeholder='Введите артикул товара')
    )
# =================================================================================================


# == Отмена добавления товара =====================================================================
# Обработчик комады /cancel для остановки машины состояний добавления товара
@router.message(
    or_f(
        Command('cancel', ignore_case=True),
        F.text.lower().contains('отменить')
    ),
    ~StateFilter(default_state),
    ~StateFilter(FSMSku.delete)
)
async def handler_cmd_cancel(message: types.Message, state: FSMContext):
    if await state.get_state() == FSMSku.name:
        await state.clear()

        await message.answer(
            text=f"❌ 📦 Добавление товара отменено!",
            reply_markup=keyboards.get_kb_sku_start()
        )
    else:
        data = await state.get_data()
        sku_data = data['sku_data']

        await message.answer(
            text=f"⁉️ Вы действительно хотите отменить добавление товара{sku_data.get_name_text2()}?",
            reply_markup=keyboards.get_kb_sku_cancel_yes_no().as_markup()
        )
    await message.delete()


# Обработчик кнопки "Да" для подтверждения остановки машины состояний добавления товара
@router.callback_query(
    F.data == "sku_cancel_btn_yes",
    ~StateFilter(default_state)
)
async def handler_sku_cancel_yes(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()

    data = await state.get_data()
    sku_data = data['sku_data']
    num_photos = len(sku_data.photos)

    await sku_data.delete_photos_from_chat()

    await state.clear()

    await callback.message.delete()
    await callback.message.answer(
        text=f"❌ 📦 Добавление товара{sku_data.get_name_text2()} отменено (удалено {num_photos} фото)!",
        reply_markup=keyboards.get_kb_sku_start()
    )


# Обработчик кнопки "Нет" для отмены остановки машины состояний добавления товара
@router.callback_query(
    F.data == "sku_cancel_btn_no",
    ~StateFilter(default_state)
)
async def handler_sku_cancel_no(callback: types.CallbackQuery):
    await callback.answer(reply_markup=keyboards.get_kb_sku_fsm())

    await callback.message.delete()
# =================================================================================================


# == Артикул товара ===============================================================================
# Обработчик состояния для ввода артикула товара
@router.message(
    StateFilter(FSMSku.name),
    F.text
)
async def handler_state_name(message: types.Message, state: FSMContext):
    data = await state.get_data()
    sku_data = data['sku_data']
    sku_data.name = message.text.strip()
    await state.set_data(data)

    await state.set_state(FSMSku.photos)

    await message.reply(
        text=f"Артикул товара: {sku_data.get_name_text()}.\n\n"
              "📸 Сфотографируйте товар!",
        reply_markup=keyboards.get_kb_sku_fsm(input_field_placeholder="Сфотографируйте товар")
    )


# Обработчик состояния для ввода артикула товара, если прислали не текст
@router.message(
    StateFilter(FSMSku.name),
    ~F.text
)
async def handler_state_name_not_text(message: types.Message):
    await message.reply(
        text=f"Это не артикул!\n\n"
             f"📝 Введите артикул товара:",
        reply_markup=keyboards.get_kb_sku_fsm(input_field_placeholder="Введите артикул товара")
    )
# =================================================================================================


# == Сохранение товара ============================================================================
# Обработчик комады /save и кнопки "Завершить добавление товара"
# для завершения машины состояний добавления товара и сохранения фото товара
@router.message(
    or_f(
        Command('save', ignore_case=True),
        F.text.lower().contains("завершить"),
        F.text.lower().contains("сохранить"),
    ),
    StateFilter(FSMSku.photos)
)
async def handler_sku_save(message: types.Message, state: FSMContext):
    data = await state.get_data()
    sku_data = data['sku_data']

    if sku_data.photos:
        await sku_data.save_photos_to_store()

        saved_files_text = ''
        for photo in sku_data.photos.values():
            saved_files_text += f"📸️ {photo.name} - разрешение: {photo.width} x {photo.height}\n"

        await state.clear()

        text = f"✅ 📦 Товар{sku_data.get_name_text2()} сохранен!\n\n" \
               f"Сохранено {len(sku_data.photos)} фото:\n" \
               f"{saved_files_text}"
        await message.answer(
            text=text,
            reply_markup=keyboards.get_kb_sku_start()
        )

        await add_log(
            user_id=message.from_user.id,
            user_name=message.from_user.full_name,
            sku=sku_data.name,
            action='save',
            description=text
        )
    else:
        await message.answer(
            text="Вы не сделали ниодного фото товара!\n\n"
                 "📸 Сфотографируйте товар!",
            reply_markup=message.reply_markup
        )

# =================================================================================================


# == Фото товара ==================================================================================
# Обработчик состояния для добавдения фото товара
@router.message(
    StateFilter(FSMSku.photos),
    F.photo
)
async def handler_sku_photos(message: types.Message, state: FSMContext):
    data = await state.get_data()
    sku_data = data['sku_data']

    sku_data.photos[message.message_id] = SkuPhoto(message=message)

    await state.set_data(data)

    await message.reply(
        text=f"✅ 📸 Фото для товара{sku_data.get_name_text2()} получено!\n\n"
             "📸 Сфотографируйте товар!",
        reply_markup=keyboards.get_kb_sku_photo_delete().as_markup()
    )


# Обработчик состояния для добавдения фото товара, если прислали не фото
@router.message(
    StateFilter(FSMSku.photos),
    ~F.photo
)
async def handler_sku_photos_not_photo(message: types.Message):
    await message.reply(
        text="Это не фото!\n\n"
             "📸 Сфотографируйте товар!",
        reply_markup=keyboards.get_kb_sku_fsm(input_field_placeholder="Сфотографируйте товар")
    )


# Обработчик кнопки "Удалить это фото" для подтверждения остановки машины состояний добавления товара
@router.callback_query(
    StateFilter(FSMSku.photos),
    F.data == "sku_photo_delete"
)
async def handler_sku_photo_delete(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()

    message = callback.message
    data = await state.get_data()
    sku_data = data['sku_data']

    if len(sku_data.photos):
        sku_data.photos.pop(message.reply_to_message.message_id)
        await state.set_data(data)

        await message.reply_to_message.reply(
            text=f"🗑️ 📸 Это фото для товара{sku_data.get_name_text2()} удалено!\n\n"
                 f"📸 Сфотографируйте товар!",
            reply_markup=keyboards.get_kb_sku_fsm(input_field_placeholder="Сфотографируйте товар")
        )
        await message.reply_to_message.delete()
        await message.delete()


# =================================================================================================


# == Удаление товара ============================================================================
# Обработчик комады /delete и кнопки "Удалить товар" для запуска машины состояний для удаления товара
@router.message(
    or_f(
        Command('delete', ignore_case=True),
        F.text.lower().contains("удалить"),
    ),
    StateFilter(default_state)
)
async def handler_sku_delete(message: types.Message, state: FSMContext):
    await state.set_state(FSMSku.delete)

    await message.delete()

    data = dict(sku_data=SkuData(store=img_folder, chat=message.chat))
    await state.set_data(data)

    await message.answer(
        text="🗑️ Начинаем удалять товар.\n\n"
             "📝 Введите артикул товара:",
        reply_markup=keyboards.get_kb_sku_delete()
    )


@router.message(
    or_f(
        Command('cancel', ignore_case=True),
        F.text.lower().contains('отменить')
    ),
    StateFilter(FSMSku.delete)
)
async def handler_state_delete_cancel(message: types.Message, state: FSMContext):
    await state.clear()

    await message.answer(
        text="❌ 📦 Удаление товара отменено!",
        reply_markup=keyboards.get_kb_sku_start()
    )
    await message.delete()


# Обработчик состояния для ввода артикула удаляемого товара
@router.message(
    StateFilter(FSMSku.delete),
    F.text
)
async def handler_state_delete(message: types.Message, state: FSMContext):
    data = await state.get_data()
    sku_data = data['sku_data']
    sku_data.name = message.text.strip()
    await state.set_data(data)

    await message.reply(
        text=f"⁉️ Вы действительно хотите удалить товар{sku_data.get_name_text2()}?",
        reply_markup=keyboards.get_kb_sku_delete_yes_no().as_markup()
    )


# Обработчик состояния для ввода артикула удаляемого товара, если прислали не текст
@router.message(
    StateFilter(FSMSku.delete),
    ~F.text
)
async def handler_state_delete_not_text(message: types.Message):
    await message.reply(
        text=f"Это не артикул!\n\n"
             f"📝 Введите артикул товара:",
        reply_markup=keyboards.get_kb_sku_delete()
    )


# Обработчик кнопки "Да" для подтверждения удаления товара
@router.callback_query(
    F.data == "sku_delete_btn_yes",
    ~StateFilter(default_state)
)
async def handler_sku_delete_yes(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()

    message = callback.message
    data = await state.get_data()
    sku_data = data['sku_data']

    deleted_files = sku_data.delete_photos_from_store()
    deleted_files_text = "\n".join(deleted_files)

    if len(deleted_files):
        text = f"❌ 📦 Товар{sku_data.get_name_text2()} удален!\n\n" \
               f" Удалено {len(deleted_files)} фото:\n" \
               f"{deleted_files_text}"
        await add_log(
            user_id=callback.from_user.id,
            user_name=callback.from_user.full_name,
            sku=sku_data.name,
            action='delete',
            description=text
        )
    else:
        text = f"⚠️ 📦 Товар{sku_data.get_name_text2()} не найден!\n"

    await state.clear()

    await message.reply(
        text=text,
        reply_markup=keyboards.get_kb_sku_start()
    )


# Обработчик кнопки "Нет" для отмены удаления товара
@router.callback_query(F.data == "sku_delete_btn_no", ~StateFilter(default_state))
async def handler_sku_delete_no(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()

    await state.clear()

    await callback.message.answer(
        text="❌ 📦 Удаление товара отменено!",
        reply_markup=keyboards.get_kb_sku_start()
    )
    await callback.message.delete()
# =================================================================================================
