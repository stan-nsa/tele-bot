# URL чтобы узнать id пользователя и id чата: https://api.telegram.org/bot<BOT-TOKEN>/getUpdates
# URL чтобы узнать информацию по апдейтам: https://api.telegram.org/bot<BOT-TOKEN>/getWebhookInfo


from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str          # Токен для доступа к телеграм-боту
    admins: list[int]   # Список id администраторов бота
    chats: list[int]    # Список id чатов бота
    bot_url: str        # URL телеграм-бота


@dataclass
class ImageConfig:
    folder: str              # Путь к директории для хранения фото
    file_name_template: str  # Шаблон имени файла фото
    resolution: int          # Разрешение фото: {1280, 800, 320, 90}


@dataclass
class DatabaseConfig:
    database: str         # Название базы данных
    db_host: str          # URL-адрес базы данных
    db_user: str          # Username пользователя базы данных
    db_password: str      # Пароль к базе данных


@dataclass
class Config:
    bot: TgBot
    img: ImageConfig
    db: DatabaseConfig
    demo: bool


env = Env()
env.read_env()


# Создаем экземпляр класса Config и наполняем его данными из переменных окружения
config = Config(
    bot=TgBot(
        token=env('BOT_TOKEN', default=''),
        admins=env.list('ADMINS', subcast=int, default=[]),
        chats=env.list('CHATS', subcast=int, default=[]),
        bot_url=env('BOT_URL', default=''),
    ),
    img=ImageConfig(
        folder=env('IMG_FOLDER', default='.'),
        file_name_template=env('IMG_FILE_NAME_TEMPLATE', default='%s_%d.jpg'),
        resolution=env.int('IMG_RESOLUTION', default=1280),
    ),
    db=DatabaseConfig(
        database=env('DATABASE', default=''),
        db_host=env('DB_HOST', default=''),
        db_user=env('DB_USER', default=''),
        db_password=env('DB_PASSWORD', default=''),
    ),
    demo=env.bool('DEMO')#, default=False),
)
