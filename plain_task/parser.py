import os
import re
import time
import asyncio

from lxml import html
from values import MAIN_URL, ALL_PAGES
from db import *

from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientError


async def get_page_urls(tree):

    ''' собираем URL всех страниц '''
    urls = list()
    count = int(await get_count_page(tree))

    for i in range(1, count+1):  # пробегаем по всем страницам
        url = ALL_PAGES.format(i)
        if url not in urls:
            urls.append(url)
    return urls


async def get_count_page(tree):

    ''' находим количество страниц '''
    pagination = [i for i in tree.xpath(LIST_PAGES)]
    match = re.search(r'[0-9]{1,2}', pagination[-1])
    count_page = match[0] if match else 'Not found'
    return count_page


async def get_text(url):

    """ получем html код страницы """
    loop = asyncio.get_running_loop()
    async with ClientSession(loop=loop) as client:
        try:
            async with client.get(url) as response:
                if response.status == 200:
                    try:
                        print(f"{url}" + "| OK ")
                        return await response.text()
                    except UnicodeDecodeError as identifier:
                        print(f"Bad decode: " + {url})
                else:
                    print(response.status)
        except ClientError as e:
            print("Error:" + e)


async def  one_time_task(MAIN_URL):
    init_db()
    result = []
    # парсим раздел

    response = await get_text(MAIN_URL)
    # узнаем ссылки на каждую страницу со статьями
    pages_urls = await get_page_urls(response)

    for uri in pages_urls:
        tasks = []
        # делаем запрос на след страницу
        res = await request_page(uri)
        # собираем ссылки на статьи
        url_posts = [i for i in res.xpath(URL_POSTS)]

        for url in url_posts:
            write_url(url)  # пишем юрл в бд
            task = asyncio.create_task(get_text(url))
            tasks.append(task)

        html_page = await asyncio.gather(*tasks)

        # тут лежат необработанные статьи
        result += html_page

    tree_result = []
    for text in result:
        try:
            tree = html.fromstring(text)
            tree_result.append(tree)
        except TypeError:
            pass

    # список обработанных статей
    result_parse = [parse_article(i) for i in tree_result]



if __name__ == "__main__":
    asyncio.run(one_time_task(MAIN_URL))
