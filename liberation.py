from datetime import date, timedelta
from time import sleep
import csv
from bs4 import BeautifulSoup
import requests
from trafilatura import extract

def get_page(url):
    url = f'https://www.liberation.fr{url}'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html5lib')

    if title := soup.select_one('h1'):
        title = title.text
    if desc := soup.select_one('div[class*=TypologyArticle__BlockContainer] span[class*=TypologyArticle__BlockSubHeadline]'):
        desc = desc.text
    #removal
    # if buttons := soup.select_one('section.article__reactions'):
        # buttons.decompose()

    if content := soup.select_one('article.article-body-wrapper'):
        content = extract(content.decode_contents(), include_comments=False)

    # print(title)
    # print(desc)
    # print(content)

    if title and desc and content:
        with open('exports/liberation.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([url, title, desc, content])

def get_links_page(date):
    url = f'https://www.liberation.fr/archives/{date}/'

    print(url)
    r = requests.get(url)
    #print(r.content)

    soup = BeautifulSoup(r.content, 'html5lib')

    articles = soup.select('body main main article')
    # print(articles)
    for article in articles:
        if article.select_one('span.color_yellow_2'):
            continue

        if link := article.select_one('a'):
            print(link['href'])
            get_page(link['href'])
            sleep(1)
            # break


today = date.today()

for i in range(90):
    day = today - timedelta(days=i)
    date = day.strftime('%Y/%m/%d')
    print(date)
    get_links_page(date)
    # break
