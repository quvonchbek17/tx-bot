from environs import Env

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

# .env fayl ichidan quyidagilarni o'qiymiz
BOT_TOKEN = env.str("BOT_TOKEN")  # Bot token
ADMINS = env.list("ADMINS")  # adminlar ro'yxati
IP = env.str("ip")  # Xosting ip manzili

DB_USER = env.str("DB_USER")
DB_PASS = env.str("DB_PASS")
DB_NAME = env.str("DB_NAME")
DB_HOST = env.str("DB_HOST")

# DB_URL = env.str("DB_URL")

# import os

# BOT_TOKEN = os.environ.get("BOT_TOKEN")  # Bot token
# ADMINS = list(os.environ.get("ADMINS").split(','))  # adminlar ro'yxati
# IP = str(os.environ.get("ip"))  # Xosting ip manzili

# DB_USER = str(os.environ.get("DB_USER"))
# DB_PASS = str(os.environ.get("DB_PASS"))
# DB_NAME = str(os.environ.get("DB_NAME"))
# DB_HOST = str(os.environ.get("DB_HOST"))