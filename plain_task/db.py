import os
import sqlite3
from values import *


def init_db():
    """ создаем таблицу """

    conn = get_conn()
    conn.cursor().executescript("""
                   CREATE TABLE IF NOT EXISTS ARTCILE(
                   ID INT AUTO_INCREMENT PRIMARY KEY ,
                   NICKNAME TEXT,
                   TITLE TEXT,
                   TXT TEXT,
                   DATE_TIME TEXT);

                   CREATE TABLE IF NOT EXISTS URLS_ARTCILES(
                   ID INT AUTO_INCREMENT PRIMARY KEY ,
                   URL TEXT); """)
    return None


def get_conn():
    conn = sqlite3.connect(os.path.join("database", "data.db"))
    return conn


def write_article(nick, title, text, date_time):
    """ пишем статью базу данных """
    conn = get_conn()
    conn.cursor().execute(
        f"INSERT INTO ARTCILE(NICKNAME, TITLE, TXT, DATE_TIME) VALUES ('{nick}','{title}','{text}','{date_time}')")
    conn.commit()


def write_url(url):
    """ пишем юрл в бд """
    conn = get_conn()
    conn.cursor().execute(
        f"INSERT INTO URLS_ARTCILES(URL) VALUES ('{url}')")
    conn.commit()


def url_in_db(url):
    """ проверяем urls """
    conn = get_conn()
    result = conn.cursor().execute(f"SELECT * FROM URLS_ARTCILES WHERE URL = '{url}';")
    if result is None:
        return False
    else:
        return True

def parse_article(answer):

    """ вытягиваем данные и передаем в функцию записи в бд """
    nickname = answer.xpath(AUTHOR)[0]
    title = answer.xpath(TITLE)[0]
    text = ''.join(answer.xpath(TEXT))
    date_time = answer.xpath(DATE_TIME)[0]
    write_article(nickname, title, text, date_time)


