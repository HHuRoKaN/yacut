import re
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import (DataRequired, Length, URL, ValidationError,
                                Optional)
from flask_wtf.file import MultipleFileField

from .constants import Validation


class LinkForm(FlaskForm):
    """Форма для коротких ссылок."""
    original_link = StringField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле'),
                    URL(message='Некорректная ссылка')]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[Length(Validation.MIN_SHORT_ID_LENGTH,
                           Validation.MAX_SHORT_ID_LENGTH),
                    Optional()]
    )
    submit = SubmitField('Создать')

    def validate_custom_id(form, field):
        if re.fullmatch(Validation.CUSTOM_ID_PATTERN, field.data) is None:
            raise ValidationError(
                'Указано недопустимое имя для короткой ссылки.'
            )


class FilesForm(FlaskForm):
    """Форма для загрузки файлов и получения коротких ссылок на них."""
    files = MultipleFileField(
        validators=[DataRequired(message='Обязательное поле')])
    submit = SubmitField('Загрузить')

    def validate_files(self, field):
        if len(field.data) > Validation.MAX_COUNT_FILES:
            raise ValidationError(
                f'Нельзя загружать больше {Validation.MAX_COUNT_FILES}'
                'файлов за раз.')
