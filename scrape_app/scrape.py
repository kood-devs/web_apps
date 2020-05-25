"""
    so function use test in python
"""
from ctypes import *
import json
import re

import numpy as np

# const params
URL_INIT = 'https://www.nikkei.com/'
NIKKEI_CATEGORY = [
    'news/category/',
    'economy/economic/',
    'economy/monetary/',
    'business/internet/',
    'business/startups/',
]
NEWS_LENGTH = 10


def reshape_so_text(text):
    text = text.decode('utf-8')
    p = re.compile(r'<[^>]*?>')
    text = p.sub("", text).replace('\u3000', '。').split()
    return text


def main_scrape():
    # so file function preparation
    lib = np.ctypeslib.load_library('libScraper.so', '.')
    lib.getNewsTitle.argtypes = (c_char_p, c_char_p)
    lib.getNewsTitle.restype = c_char_p

    # 日経新聞
    contents = dict()
    for category in NIKKEI_CATEGORY:
        url = URL_INIT + category
        url = url.encode('utf-8')

        # タイトル
        keyword = '<span class=\"m-miM09_titleL\">'
        keyword = keyword.encode('utf-8')
        text_title = lib.getNewsTitle(url, keyword)
        text_title = reshape_so_text(text_title)[:NEWS_LENGTH]

        # 本文冒頭
        keyword = 'class=\"cmnc-continue\">…続き</a>'
        keyword = keyword.encode('utf-8')
        text_abs = lib.getNewsTitle(url, keyword)
        text_abs = reshape_so_text(text_abs)[:NEWS_LENGTH]

        # リンクURL
        keyword = 'class=\"cmnc-continue\">…続き</a>'
        keyword = keyword.encode('utf-8')
        text_url = lib.getNewsTitle(url, keyword)
        text_url = text_url.decode('utf-8')

        hrefs = []
        for t in text_url.split():
            res = re.match(r'.*href=\"(.*?)".*', t)
            if res:
                hrefs.append(URL_INIT + res.group(1))
        hrefs = hrefs[:NEWS_LENGTH]

        for title, abstract in zip(text_title, text_abs):
            contents[title.replace('［有料会員限定］', '')] = [abstract, hrefs]

    return contents
