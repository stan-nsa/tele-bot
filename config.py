from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env('BOT_TOKEN', default='')

IMG_RESOLUTION = env.int('IMG_RESOLUTION', default=1280)
IMG_FOLDER = env('IMG_FOLDER', default='.')

IMG_FILE_NAME_TEMPLATE = env('IMG_FILE_NAME_TEMPLATE', default='%s-%d.jpg')

ADMIN = env.int('ADMIN', default=0)
USERS = env.list('USERS', subcast=int, default=[])
