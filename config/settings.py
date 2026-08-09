import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

MAX_FILE_SIZE = 10 * 1024 * 1024
TEMP_DIR = "data/temp/"
