# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

url_base = "https://m.bqg334.com/list/"  # 小说索引页
url_end = ".html"
page = range(174, 294)  # 第三部是174-294页
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.289 Safari/537.36'
}
session = ""


def init():
    global session
    session = requests.session()


def get_url_text(url):
    content = session.get(url, headers=headers).content
    soup = BeautifulSoup(content)
    return soup.text


def clean_text(text, index):
    try:
        keywords = "请收藏：https://m.bqg334.com"
        result = text.split(keywords)[0]
        keywords = "字体：大 中 小"
        result_1 = result.split(keywords)[0]
        result_2 = result.split(keywords)[1]
        keywords = "下一章"
        result_2 = result_2.split(keywords)[1]
        if index == 1:
            keywords = "www．．"
            result_2 = result_2.split(keywords)[1]
            return result_1 + result_2
        else:
            return result_2
    except IndexError:
        # 处理 IndexError 异常
        print("发生了 IndexError 错误:", IndexError)
        return "error"


def get_text():
    init()
    texts = ""
    max_context = 50
    max_sub_context = 20
    for i in range(1, max_context):
        print("data " + str(i))
        err_acc = 0
        for j in range(0, max_sub_context):
            strTemp = "_" + str(j)
            if j == 0:
                strTemp = ""
            strTemp = str(i) + strTemp
            url = url_base + strTemp + url_end
            text = "\n" + strTemp + "\n" + get_url_text(url)
            text = clean_text(text, j)
            if text == "error":
                err_acc = err_acc + 1
                print("error:" + strTemp)
                texts = texts + "\n error \n"
                if err_acc < 3:
                    continue
                else:
                    break
            texts = texts + text
    texts= texts.replace('　　', '\n  ')
    f = open("b.txt", "w", encoding="utf-8")
    f.write(str(texts).replace('\n\n', '\n'))
    f.close()


# 运行程序
if __name__ == '__main__':
    get_text()
