from random import choices
from flask import request

from .models import URLMap
from .constants import Validation


def get_unique_short_id():
    """Генерация короткой ссылки."""
    sequence = ''.join(choices(Validation.ALLOWED_CHARACTERS,
                               k=Validation.DEFAULT_SHORT_ID_LENGTH))
    if URLMap.query.filter_by(short=sequence).first() is None:
        return sequence
    return get_unique_short_id()


def get_host_url():
    """Получение имени хоста."""
    return str(request.host_url)
