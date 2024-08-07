from aiogram.types import BotCommand


commands_menu = [BotCommand(command='start', description='Запуск бота'),
                 BotCommand(command='help', description='Помощь'),
                 BotCommand(command='add', description='Добавить товар'),
                 BotCommand(command='save', description='Сохранить товар'),
                 BotCommand(command='cancel', description='Отменить'),
                 BotCommand(command='delete', description='Удалить товар'),
                 BotCommand(command='admin', description='Админское меню'),
                 ]
