import csv
from time import sleep
from bs4 import BeautifulSoup
import requests


for i in range(1, 11):
    url = f'https://www.francetvinfo.fr/decouverte/bizarre/'

    if i > 1:
        url += f'{i}.html'

    print(url)

    r = requests.get(url)

    soup = BeautifulSoup(r.text, 'html5lib')

    articles = soup.select('main section.taxonomy-contents article a')
    # print(articles)

    contents = []
    for article in articles:
        content = {
            'url': 'https://www.francetvinfo.fr{}'.format(article['href']),
            'title': article.select_one('p.card-article-list-l__title').text.strip()
        }
        contents.append(content)

    # print (contents)

    # break

    with open('exports/franceinfotv_bizarre.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        for content in contents:
            writer.writerow([content['url'], content['title']])

    sleep(1)
