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


def index(req):
    return render(req, 'trialTaskApp/index.html', {'toi_news': toi_news})
