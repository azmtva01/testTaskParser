from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

# Getting articles from Habr

r = requests.get("https://habr.com/ru/all/")
soup = BeautifulSoup(r.content, 'html.parser')
headings = soup.find_all('h2')
toi_headings = headings[0:-13]
news = []

for i in toi_headings:
    news.append(i.text)


def index(req):
    return render(req, 'trialTaskApp/index.html', {'news': news})
