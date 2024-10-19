from datetime import date, timedelta
from time import sleep
import csv
from bs4 import BeautifulSoup
import requests
from trafilatura import extract


def get_articles(date):
    url = f'https://www.liberation.fr/archives/{date}/'

    print(url)
    r = requests.get(url)
    #print(r.content)

    soup = BeautifulSoup(r.text, 'html5lib')

    articles = soup.select('body main main article')
    # print(articles)
    for article in articles:
        if (link := article.select_one('a')) and (title := link.select_one('h2')):
            # print('https://www.liberation.fr{}'.format(link['href']))
            # print(title.text.strip())
            # break

            if link['href'] and title.text:
                with open('exports/liberation.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['https://www.liberation.fr{}'.format(link['href']), title.text.strip()])

today = date.today()

for i in range(90):
    day = today - timedelta(days=i)
    date = day.strftime('%Y/%m/%d')
    print(date)
    get_articles(date)
    sleep(1)
    # break
