

MAIN_URL = "https://habr.com/ru/flows/develop/"
ALL_PAGES = "https://habr.com/ru/flows/develop/page{}"
TIME_SLEEP = 18000 # 5 часов


URL_POSTS = '//li/article[contains(@class, "post_preview")]/h2/a/@href'
LIST_PAGES = '//ul[@class="toggle-menu toggle-menu_pagination"]//a[last()]/@href'

AUTHOR = "//div[contains(@class, 'post__wrapper')]/header[contains(@class, 'post__meta')]" \
         "/a[contains(@class, 'post__user-info')]/span[contains(@class, 'user-info__nickname')]/text()"

TITLE = "//div[contains(@class, 'post__wrapper')]/h1[contains(@class, 'post__title_full')]/span/text()"
TEXT = "//div[contains(@class, 'post__text post__text-html post__text_v1')]//text()"
DATE_TIME = "//div[contains(@class, 'post__wrapper')]/header[contains(@class, 'post__meta')]" \
            "/span[contains(@class, 'post__time')]/text()"
