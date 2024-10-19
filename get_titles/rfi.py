from datetime import date, timedelta
from time import sleep
import csv, re
from bs4 import BeautifulSoup
import requests
from unidecode import unidecode
from babel.dates import format_datetime


def get_articles(year, month, date):
    url = f'https://www.rfi.fr/fr/archives/{year}/{month}/{date}'

    print(url)

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:131.0) Gecko/20100101 Firefox/131.0',
        'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
        'Connection': 'keep-alive',
    }

    r = requests.get(url, headers=headers)

    # print(r.status_code)
    # print(r.text)
    if r.status_code != 200:
        return
    #print(r.content)

    soup = BeautifulSoup(r.text, 'html5lib')

    articles = soup.select('div.o-archive-day ul.o-archive-day__list li a')
    # print(articles)

    contents = []
    for article in articles:
        content = {
            'url': 'https://www.rfi.fr{}'.format(article['href']),
            'title': article.text.strip()
        }
        contents.append(content)

    # print (contents)

    with open('exports/rfi.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        for content in contents:
            writer.writerow([content['url'], content['title']])

today = date.today()

for i in range(90):
    day = today - timedelta(days=i)
    year = day.strftime('%Y')
    month = day.strftime('%m')
    date = unidecode(format_datetime(day, 'dd-MMMM-Y', locale='fr_FR'))
    print()
    print(date)
    get_articles(year, month, date)
    sleep(1)
    # break
