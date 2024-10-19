from datetime import date, timedelta
from time import sleep
import csv, re
from bs4 import BeautifulSoup
import requests
from unidecode import unidecode
from babel.dates import format_datetime
from unicodedata import normalize


def get_articles(date, page = None):
    url = 'https://www.ouest-france.fr/archives/{}/{}/'.format(re.sub(r'^.+\-(\d+)$', r'\1', date), date)

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:131.0) Gecko/20100101 Firefox/131.0',
        'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
        'Connection': 'keep-alive',
    }

    if page is not None:
        url = f'{url}?page={page}'

    print(url)

    r = requests.get(url, headers=headers)
    #print(r.content)

    # print(r.text)
    soup = BeautifulSoup(r.text, 'html5lib')

    articles = soup.select('section.liste-articles article a.titre-lien')
    # print(articles)

    contents = []
    for article in articles:

        if inner_h2 := article.select_one('h2 > *'):
            inner_h2.decompose()

        content = {
            'url': article['href'],
            'title': normalize('NFKD', article.text.strip())
        }
        contents.append(content)
        # get_page(article['href'])
        # sleep(1)
        # break

    print (len(contents))

    with open('exports/ouest_france.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        for content in contents:
            writer.writerow([content['url'], content['title']])

    sleep(1)

    if page is not None:
        return

    pager = soup.select_one('div #bloc_3quarts_1_pagination nav.su-pagination')

    if not pager:
        return

    page_links = pager.select('ul > li.su-page-select > ul.su-pages-list > li')

    print('pages : {}'.format(len(page_links)))

    if len(page_links) < 2:
        return

    for i in range(2, len(page_links) + 1):
        get_articles(date, i)

today = date.today()

for i in range(90):
    day = today - timedelta(days=i)
    date = unidecode(format_datetime(day, 'dd-MMMM-Y', locale='fr_FR'))
    print()
    print(date)
    get_articles(date)
    sleep(1)
    # break
