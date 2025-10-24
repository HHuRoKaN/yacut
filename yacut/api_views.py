import re
from urllib.parse import urljoin
from flask import jsonify, request

from . import app, db
from .models import URLMap
from .utils import get_unique_short_id
from .error_handlers import InvalidAPiUsage
from .constants import Validation, HTTPStatus


@app.route('/api/id/', methods=['POST'])
def create_link():
    """API создания короткой ссылки."""
    if not request.data:
        raise InvalidAPiUsage('Отсутствует тело запроса',
                              HTTPStatus.BAD_REQUEST)
    data = request.get_json()
    if not data.get('url'):
        raise InvalidAPiUsage('\"url\" является обязательным полем!',
                              HTTPStatus.BAD_REQUEST)
    if not data.get('custom_id'):
        custom_id = get_unique_short_id()
    if data.get('custom_id'):
        if not re.match(
            Validation.CUSTOM_ID_PATTERN, data.get('custom_id')) or len(
           data.get('custom_id')) > Validation.MAX_SHORT_ID_LENGTH:
            raise InvalidAPiUsage(
                'Указано недопустимое имя для короткой ссылки',
                HTTPStatus.BAD_REQUEST)
        else:
            custom_id = data['custom_id']
    if URLMap.query.filter_by(short=custom_id).first() is not None:
        raise InvalidAPiUsage(
            'Предложенный вариант короткой ссылки уже существует.')
    urlmap = URLMap(
        original=data['url'],
        short=custom_id
    )
    db.session.add(urlmap)
    db.session.commit()
    return jsonify(
        dict(url=data['url'], short_link=urljoin(request.url_root, custom_id))
    ), HTTPStatus.CREATED


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original_link(short_id):
    """API получения оригинальной ссылки по короткой."""
    urlmap = URLMap.query.filter_by(short=short_id).first()
    if urlmap is None:
        raise InvalidAPiUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': urlmap.original}), HTTPStatus.OK
