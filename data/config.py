from environs import Env
from dotenv import set_key, get_key
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# environs kutubxonasidan foydalanish
env = Env()
env.read_env()
# .env fayl ichidan quyidagilarni o'qiymiz
BOT_TOKEN = env.str("BOT_TOKEN")  # Bot toekn
ADMINS = env.list("ADMINS")  # adminlar ro'yxati
# print(ADMINS)
IP = env.str("IP")  # Xosting ip manzili
ACCESS_TOKEN = env.str("ACCESS_TOKEN")

def add_admin_to_dotenv(value: str):
    # get the existing value
    existing_value = get_key(f"{BASE_DIR}/.env", 'ADMINS')
    new_value = existing_value + f",{value}"
    set_key(f"{BASE_DIR}/.env", 'ADMINS', new_value)


def remove_admin(value: str):
    # get the existing value
    existing_value = get_admins()
    existing_value.remove(value)
    new_value = ','.join(existing_value)
    set_key(f"{BASE_DIR}/.env", 'ADMINS', new_value)


def get_admins() -> list:
    return get_key(f"{BASE_DIR}/.env", 'ADMINS').split(',')


DB_USER = env.str("DB_USER")
DB_PASS = env.str("DB_PASS")
DB_NAME = env.str("DB_NAME")
DB_HOST = env.str("DB_HOST")

# admins = get_admins()
# index = admins.index('1211541928')
# print(index)
# print(get_admins())
# add_admin_to_dotenv('1211541928')
# print(get_admins())
# remove_admin('1211541928')
# print(set(get_admins()))
