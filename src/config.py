import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

# Database constants
BASE_DIR = Path().resolve()
SQLITE_DB_FILE = BASE_DIR / "database/db.sqlite"
DATE_FORMAT = "%d.%m.%Y %H:%M:%S"

# Game constants
MAX_VOTES = 10
MAX_HITLER_VOTERS = 1
MIN_HITLER_VOTERS = 1
MAX_LIBERAL_VOTERS = 6
MIN_LIBERAL_VOTERS = 3
MAX_FASCIST_VOTERS = 3
MIN_FASCIST_VOTERS = 1
