from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env('BOT_TOKEN')

IMG_FOLDER = env('IMG_FOLDER')

IMG_FILE_NAME_TEMPLATE = env('IMG_FILE_NAME_TEMPLATE')

# inline