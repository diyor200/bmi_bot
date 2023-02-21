from environs import Env
from pathlib import Path

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()
# .env fayl ichidan quyidagilarni o'qiymiz
BOT_TOKEN = env.str("BOT_TOKEN")  # Bot toekn
ADMINS = env.list("ADMINS")  # adminlar ro'yxati
IP = env.str("ip")  # Xosting ip manzili

DB_USER = env.str("DB_USER")
DB_PASS = env.str("DB_PASS")
DB_NAME = env.str("DB_NAME")
DB_HOST = env.str("DB_HOST")


class AdminList:

    def __init__(self):
        self.admins = ["5697570359"]

    def return_list(self):
        print(self.admins)

    def add_element(self, var):
        copy_admins = self.admins.copy()
        copy_admins.append(var)
        self.admins = copy_admins
        # print(self.admins)
        return True


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
print(BASE_DIR)
