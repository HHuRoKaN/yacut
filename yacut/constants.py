import os
from string import ascii_letters, digits
from dotenv import load_dotenv


class Validation:
    """Константы валидации."""
    ALLOWED_CHARACTERS = ascii_letters + digits
    DEFAULT_SHORT_ID_LENGTH = 6
    MIN_SHORT_ID_LENGTH = 0
    MAX_SHORT_ID_LENGTH = 16
    CUSTOM_ID_PATTERN = r'^[A-Za-z0-9]+$'
    MAX_COUNT_FILES = 10
    MAX_LENGTH_STRING_BD = 128


class YaDisk:
    """Константы Яндекс Диска."""
    API_HOST = 'https://cloud-api.yandex.net/'
    API_VERSION = 'v1'
    REQUEST_UPLOAD_URL = f'{API_HOST}{API_VERSION}/disk/resources/upload'
    DOWNLOAD_LINK_URL = f'{API_HOST}{API_VERSION}/disk/resources/download'
    load_dotenv()
    DISK_TOKEN = os.environ.get('DISK_TOKEN')
    AUTH_HEADERS = {'Authorization': f'OAuth {DISK_TOKEN}'}


class HTTPStatus:
    """Константы кодов ошибок."""
    BAD_REQUEST = 400
    CREATED = 201
    OK = 200
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500
