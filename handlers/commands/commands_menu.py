from aiogram.types import BotCommand


commands_menu = [BotCommand(command='start', description='Запуск бота'),
                 BotCommand(command='help', description='Помощь'),
                 BotCommand(command='admin', description='Админское меню'),
                 BotCommand(command='add', description='Добавить товар'),
                 BotCommand(command='save', description='Сохранить товар'),
                 ]
