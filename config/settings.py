import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()

admin_raw = os.getenv("ADMIN_ID", "0").strip()
try:
    ADMIN_ID = int(admin_raw) if admin_raw else 0
except ValueError:
    ADMIN_ID = 0

MAX_FILE_SIZE = 10 * 1024 * 1024
TEMP_DIR = "data/temp/"

