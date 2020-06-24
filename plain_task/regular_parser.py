import asyncio
from lxml import html
from values import MAIN_URL, TIME_SLEEP
from parser import *
from db import *
from time import sleep

async def regular_task(MAIN_URL):

    result = []
    tasks = []
    # парсим раздел
    response = await request_page(MAIN_URL)
    # собираем ссылки на статьи
    url_posts = [i for i in response.xpath(URL_POSTS)]

    for url in url_posts:
        if not url_in_db(url):# проверяем в бд юрл
            write_url(url)     

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
    while True:
        sleep(TIME_SLEEP)
        asyncio.run(regular_task(MAIN_URL))
        
