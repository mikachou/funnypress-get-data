from datetime import date, timedelta
from time import sleep
import csv
from bs4 import BeautifulSoup
import requests


def get_articles(date):
    url = f'https://www.ladepeche.fr/articles/{date}/'

    print(url)
    r = requests.get(url)
    #print(r.content)

    soup = BeautifulSoup(r.text, 'html5lib')

    articles = soup.select('div.section a')
    # print(articles)

    contents = []
    for article in articles:
        content = {
            'url': 'https://www.ladepeche.fr{}'.format(article['href']),
            'title': article.text.strip()
        }
        contents.append(content)

    # print(contents)

    with open('exports/la_depeche.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        for content in contents:
            writer.writerow([content['url'], content['title']])

today = date.today()

for i in range(90):
    day = today - timedelta(days=i)
    date = day.strftime('%Y/%m/%d')
    print(date)
    get_articles(date)
    sleep(1)
    # break
