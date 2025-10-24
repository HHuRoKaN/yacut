from flask import flash, redirect, render_template
import asyncio

from . import app, db
from .forms import LinkForm, FilesForm
from .models import URLMap, Files
from .utils import get_unique_short_id, get_host_url
from .ya_disk import upload_files, download_files


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """Обработчик главной страницы приложения."""
    form = LinkForm()
    if form.validate_on_submit():
        if form.custom_id.data:
            custom_id = form.custom_id.data
            if URLMap.query.filter_by(short=custom_id).first() is not None:
                flash('Предложенный вариант короткой ссылки уже существует.',
                      'duplication')
                return render_template('index.html', form=form)
        else:
            custom_id = get_unique_short_id()
        short = get_host_url() + custom_id
        urlmap = URLMap(
            original=form.original_link.data,
            short=custom_id
        )
        db.session.add(urlmap)
        db.session.commit()
        new_link = short
        flash('Ваша новая ссылка готова:', 'link-ready')
        return render_template('index.html', form=form, link=new_link)
    return render_template('index.html', form=form)


@app.route('/<short_id>', methods=['GET'])
def redirect_view(short_id):
    """Обработчик короткой ссылки."""
    urlmap = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(urlmap.original)


@app.route('/files', methods=['GET', 'POST'])
def files_view():
    """Обработчик загрузки файлов."""
    form = FilesForm()
    if form.validate_on_submit():
        original_filenames = [file.filename for file in form.files.data]
        urls = asyncio.run(upload_files(form.files.data))
        download_urls = asyncio.run(download_files(urls))
        file_record = Files(
            files=download_urls
        )
        db.session.add(file_record)
        db.session.commit()
        new_links = []
        for i, download_url in enumerate(download_urls):
            short = get_unique_short_id()
            urlmap = URLMap(
                original=download_url,
                short=short
            )
            new_links.append({'url': get_host_url() + short,
                              'filename': original_filenames[i]
                              })
            db.session.add(urlmap)
            db.session.commit()
        return render_template('files_link.html', form=form,
                               links=new_links)
    return render_template('files_link.html', form=form)
