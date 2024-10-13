from datetime import date, timedelta
from time import sleep
import csv
from bs4 import BeautifulSoup
import requests
from trafilatura import extract

def get_page(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html5lib')

    if title := soup.select_one('h1.article__title'):
        title = title.text
    if desc := soup.select_one('p.article__desc'):
        desc = desc.text
    #removal
    if buttons := soup.select_one('section.article__reactions'):
        buttons.decompose()

    if content := soup.select_one('.article__content'):
        content = extract(content.decode_contents(), include_comments=False)

    # print(title)
    # print(desc)
    # print(content)

    if title and desc and content:
        with open('exports/le_monde.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([url, title, desc, content])

def get_links_page(date, page = None):
    if page is None:
        url = f'https://www.lemonde.fr/archives-du-monde/{date}/'
    else:
        url = f'https://www.lemonde.fr/archives-du-monde/{date}/{page}/'

    print(url)
    r = requests.get(url)
    #print(r.content)

    soup = BeautifulSoup(r.content, 'html5lib')

    articles = soup.select('section#river section.teaser')
    #print(articles)
    for article in articles:
        if article.select_one('span.flag-live-cartridge__label') or article.select_one('span.icon__premium'):
            continue

        teaser_ticker = article.select_one('span.teaser__kicker')

        if teaser_ticker and teaser_ticker.text == 'Podcast':
            continue

        if link := article.select_one('a.teaser__link'):
            print(link['href'])
            get_page(link['href'])
            sleep(1)
            # break

    if page is not None:
        return

    pager = soup.select_one('section.river__pagination')

    if not pager:
        return

    page_links = pager.select('a.river__pagination--page')

    if len(page_links) < 2:
        return

    for i in range(2, len(page_links) + 1):
        get_links_page(date, i)

today = date.today()

for i in range(90):
    day = today - timedelta(days=i)
    date = day.strftime('%d-%m-%Y')
    print(date)
    get_links_page(date)
    # break
