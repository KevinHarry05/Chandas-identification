from pathlib import Path
from dotenv import load_dotenv
import os

# Go up to project root safely
BASE_DIR = Path(__file__).resolve()
while BASE_DIR.name != "chandas_project":
    BASE_DIR = BASE_DIR.parent

# Load backend/.env
ENV_PATH = BASE_DIR / "backend" / ".env"
load_dotenv(ENV_PATH)

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

# Defensive check (VERY IMPORTANT)
if not all([DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT]):
    raise RuntimeError("Database environment variables not loaded correctly")

DB_CONFIG = {
    "dbname": DB_NAME,
    "user": DB_USER,
    "password": DB_PASSWORD,
    "host": DB_HOST,
    "port": int(DB_PORT),
}
