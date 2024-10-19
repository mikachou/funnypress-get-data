from datetime import date, timedelta
from time import sleep
import csv, re
from bs4 import BeautifulSoup
import requests
from unidecode import unidecode
from babel.dates import format_datetime


def get_articles(date):
    url = 'https://www.francetvinfo.fr/archives/{}/{}.html'.format(re.sub(r'^.+\-(\d+)$', r'\1', date), date)

    print(url)
    r = requests.get(url)
    #print(r.content)

    soup = BeautifulSoup(r.content, 'html5lib')

    articles = soup.select('div.page-archives ul.page-archives__day-links li article a')
    # print(articles)

    contents = []
    for article in articles:
        if svg := article.select_one('svg.card-article__external-icon'):
            svg.decompose()
        if span := article.select_one('span.sr-only'):
            span.decompose()
        content = {
            'url': 'https://www.francetvinfo.fr{}'.format(article['href']),
            'title': article.text.strip()
        }
        contents.append(content)
        # get_page(article['href'])
        # sleep(1)
        # break

    # print (contents)

    with open('exports/franceinfotv.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        for content in contents:
            writer.writerow([content['url'], content['title']])

today = date.today()

for i in range(90):
    day = today - timedelta(days=i)
    date = unidecode(format_datetime(day, 'dd-MMMM-Y', locale='fr_FR'))
    print()
    print(date)
    get_articles(date)
    sleep(1)
    # break
