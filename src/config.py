import os
from pathlib import Path

from dotenv import load_dotenv


dotenv_path = '.env'
load_dotenv(dotenv_path)


class Config:
    """Настройки."""

    APP_HOST = os.environ.get('APP_HOST', 'localhost')
    APP_PORT = int(os.environ.get('APP_PORT', '8001'))
    BASE_DIR = Path(__file__).resolve().parent
    SERVER_DIR = Path(BASE_DIR / 'server_media')
    CLIENT_DIR = Path(BASE_DIR / 'client_media')
    SIZE = int(os.environ.get('SIZE', '100000'))


if not Path(Config.SERVER_DIR).exists():
    Path(Config.SERVER_DIR).mkdir(exist_ok=True)

if not Path(Config.CLIENT_DIR).exists():
    Path(Config.CLIENT_DIR).mkdir(exist_ok=True)
