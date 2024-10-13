from datetime import date, timedelta
from time import sleep
import csv
from bs4 import BeautifulSoup
import requests
from trafilatura import extract

def get_page(url):
    url = f'https://www.ladepeche.fr{url}'

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html5lib')

    if soup.select_one('#paywall') or soup.select_one('body.body--shopping'):
        return

    print(url)

    #removal
    if l_essentiel := soup.select_one('main article div.article-full__body span.article-full__chapo-label'):
        l_essentiel.decompose()

    if title := soup.select_one('main article h1.article-full__title'):
        title = title.text.strip()
    if desc := soup.select_one('main article div.article-full__body p.article-full__chapo'):
        desc = desc.text.strip()

    #removal
    if a_lire_aussi := soup.select('main article div.article-full__body p.std-elt__inline'):
        for elm in a_lire_aussi:
            elm.decompose()

    if extemb := soup.select('main article div.article-full__body div.extemb-container'):
        for elm in extemb:
            elm.decompose()

    if content := soup.select_one('main article div.article-full__body-content'):
        if extracted_content := extract(content.decode_contents()):
            content = extracted_content
        else:
            content = content.text.strip()

    # print(title)
    # print(desc)
    # print(content)

    if title and content:
        with open('exports/la_depeche.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([url, title, desc, content])

def get_links_page(date):
    url = f'https://www.ladepeche.fr/articles/{date}/'

    print(url)
    r = requests.get(url)
    #print(r.content)

    soup = BeautifulSoup(r.content, 'html5lib')

    articles = soup.select('div.section a')
    # print(articles)
    for article in articles:
        # print(article['href'])
        get_page(article['href'])
        sleep(1)
        # break


today = date.today()

for i in range(90):
    day = today - timedelta(days=i)
    date = day.strftime('%Y/%m/%d')
    print(date)
    get_links_page(date)
    # break
