from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

# Getting articles from Habr

toi_r = requests.get("https://habr.com/ru/all/")
toi_soup = BeautifulSoup(toi_r.content, 'html5lib')
toi_headings = toi_soup.find_all('h2')
toi_headings = toi_headings[0:-13]
toi_news = []

for th in toi_headings:
    toi_news.append(th.text)

page = 1

# while True:
#     r = requests.get("https://habr.com/ru/all/page" + str(page))
#     html = BeautifulSoup(r.content, 'html5lib')
#     items = html.select(".tm-articles-list > .tm-article-snippet")
#     # toi_r = requests.get("https://habr.com/ru/all/")
#     toi_soup = BeautifulSoup(toi_r.content, 'html5lib')
#     toi_headings = toi_soup.find_all('h2')
#     toi_headings = toi_headings[0:-13]
#     toi_news = []
#
#     if len(items):
#         for el in items:
#             title = el.select('.caption > a')
#             print(title[0].text)
#         page += 1
#     else:
#         break


def download_document(pid):
    """ Download and process a Habr document and its comments """
    # выгрузка документа
    r = requests.get('https://habrahabr.ru/post/' + str(pid) + '/')
    # парсинг документа
    soup = BeautifulSoup(r.text, 'html5lib') # instead of html.parser
    doc = {}
    doc['id'] = pid
    if not soup.find("span", {"class": "post__title-text"}):
        # такое бывает, если статья не существовала или удалена
        doc['status'] = 'title_not_found'
    else:
        doc['status'] = 'ok'
        doc['title'] = soup.find("span", {"class": "post__title-text"}).text
        doc['text'] = soup.find("div", {"class": "post__text"}).text
        doc['time'] = soup.find("span", {"class": "post__time"}).text
        # create other fields: hubs, tags, views, comments, votes, etc.
        # ...
    # сохранение результата в отдельный файл
    fname = r'files/' + str(pid) + '.pkl'
    with open(fname, 'wb') as f:
        pickle.dump(doc, f)

# Getting news from Habr


ht_r = requests.get("https://habr.com/ru/news/")
ht_soup = BeautifulSoup(ht_r.content, 'html5lib')
ht_headings = ht_soup.findAll("div", {"class": "headingfour"})
ht_headings = ht_headings[2:]
ht_news = []

for hth in ht_headings:
    ht_news.append(hth.text)


def index(req):
    return render(req, 'trialTaskApp/index.html', {'toi_news': toi_news, 'ht_news': ht_news})
