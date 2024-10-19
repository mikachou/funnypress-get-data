from datetime import date, timedelta
from time import sleep
import csv, re
from bs4 import BeautifulSoup
import requests
from unicodedata import normalize


def get_articles(date):
    url = 'https://www.leparisien.fr/archives/{}/{}'.format(re.sub(r'^.+-(\d{4})$', r'\1', date), date)

    print(url)
    r = requests.get(url)
    # r.encoding = 'utf-8'
    #print(r.content)

    soup = BeautifulSoup(r.text, 'html5lib')

    articles = soup.select('div#top div.story-preview a')
    # print(articles)

    contents = []
    for article in articles:
        content = {
            'url': 'https:{}'.format(article['href']),
            'title': normalize('NFKD', article.text.strip())
        }
        contents.append(content)
        # get_page(article['href'])
        # sleep(1)
        # break

    # print (contents)

    with open('exports/le_parisien.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        for content in contents:
            writer.writerow([content['url'], content['title']])

today = date.today()

for i in range(90):
    day = today - timedelta(days=i)
    date = day.strftime('%d-%m-%Y')
    print()
    print(date)
    get_articles(date)
    sleep(1)
    # break
