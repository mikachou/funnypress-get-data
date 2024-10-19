import csv
from time import sleep
from bs4 import BeautifulSoup
import requests


for i in range(1, 158):
    url = f'https://www.demotivateur.fr/insolite/{i}'

    print(url)

    r = requests.get(url)

    soup = BeautifulSoup(r.text, 'html5lib')

    articles = soup.select('div.main div.row a[href*="/insolite/"]')
    # print(articles)

    contents = []
    for article in articles:
        content = {
            'url': 'https://www.rfi.fr{}'.format(article['href']),
            'title': article.select_one('h2').text.strip()
        }
        contents.append(content)

    # print (contents)

    with open('exports/demotivateur.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        for content in contents:
            writer.writerow([content['url'], content['title']])

    sleep(1)
