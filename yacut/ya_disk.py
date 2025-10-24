import urllib
import asyncio
import aiohttp

from .constants import YaDisk


async def upload_files(files):
    """Список команд для асинхронной загрузки."""
    locations = []
    if files is not None:
        async with aiohttp.ClientSession() as session:
            tasks = []
            for file_obj in files:
                task = asyncio.create_task(upload_single_file(session,
                                                              file_obj))
                tasks.append(task)
            locations = await asyncio.gather(*tasks)
    return locations


async def upload_single_file(session, file_obj):
    """Асинхронная загрузка файлов."""
    payload = {
        'path': f'app:/{file_obj.filename}',
        'overwrite': 'True'
    }
    async with session.get(
        headers=YaDisk.AUTH_HEADERS,
        params=payload,
        url=YaDisk.REQUEST_UPLOAD_URL
    ) as response:
        data = await response.json()
        upload_url = data['href']
    file_obj.seek(0)
    file_content = file_obj.read()
    async with session.put(
        upload_url,
        data=file_content,
        headers={'Content-Type': 'application/octet-stream'}
    ) as response:
        location = response.headers.get('Location')
        location = urllib.parse.unquote(location)
        location = location.replace('/disk', '')
        return location


async def download_files(links):
    """Список команд для асинхронного получения ссылок."""
    urls = []
    if links:
        async with aiohttp.ClientSession() as session:
            tasks = []
            for link in links:
                task = asyncio.create_task(get_download_link(session, link))
                tasks.append(task)
            urls = await asyncio.gather(*tasks)
    return urls


async def get_download_link(session, link):
    """Асинхронное получение ссылок."""
    async with session.get(
        headers=YaDisk.AUTH_HEADERS,
        url=YaDisk.DOWNLOAD_LINK_URL,
        params={'path': link}
    ) as response:
        data = await response.json()
        download_url = data['href']
        return download_url
