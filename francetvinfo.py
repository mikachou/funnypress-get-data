from datetime import date, timedelta
from time import sleep
import csv, re
from bs4 import BeautifulSoup
import requests
from trafilatura import extract
from unidecode import unidecode
from babel.dates import format_datetime

def get_page(url):
    url = f'https://www.francetvinfo.fr{url}'

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html5lib')

    print(url)

    if badge := soup.select_one('main article h1.c-title span.badge'):
        badge.decompose()

    if title := soup.select_one('main article h1.c-title'):
        title = title.text.strip()
    if desc := soup.select_one('main article div.c-chapo'):
        desc = desc.text.strip()

    if content := soup.select_one('main article div.c-body'):
        content = extract(content.decode_contents(), include_comments=False)

    # print(title)
    # print(desc)
    # print(content)
    # print()

    if title and content:
        with open('exports/francetvinfo.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([url, title, desc, content])

def get_links_page(date):
    url = 'https://www.francetvinfo.fr/archives/{}/{}.html'.format(re.sub(r'^.+\-(\d+)$', r'\1', date), date)

    print(url)
    r = requests.get(url)
    #print(r.content)

    soup = BeautifulSoup(r.content, 'html5lib')

    articles = soup.select('div.page-archives ul.page-archives__day-links li article a')
    # print(articles)
    for article in articles:
        if any(substring in article['href'] for substring in ('/replay-jt/', '/replay-magazine/', '/meteo/meteo-france-2/', '/replay-radio/')):
            continue
        # print(article['href'])
        get_page(article['href'])
        sleep(1)
        # break


today = date.today()

for i in range(90):
    day = today - timedelta(days=i)
    date = unidecode(format_datetime(day, 'dd-MMMM-Y', locale='fr_FR'))
    print()
    print(date)
    get_links_page(date)
    # break
