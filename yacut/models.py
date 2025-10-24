from datetime import datetime

from yacut import db
from .constants import Validation


class URLMap(db.Model):
    """Модель хранения коротких ссылок."""
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(Validation.MAX_LENGTH_STRING_BD),
                         nullable=False)
    short = db.Column(db.String(Validation.MAX_LENGTH_STRING_BD))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)


class Files(db.Model):
    """Модель хранения длинных ссылок для скачивания."""
    id = db.Column(db.Integer, primary_key=True)
    files = db.Column(db.JSON)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
