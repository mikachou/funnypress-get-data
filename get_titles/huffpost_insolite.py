import csv
from time import sleep
from bs4 import BeautifulSoup
import requests
from unicodedata import normalize


page = 0
while (True):
    if page == 1:
        url = f'https://www.huffingtonpost.fr/insolite/'
    else:
        url = f'https://www.huffingtonpost.fr/insolite/?page={page}'

    print(url)

    tries = 0
    success = False
    while (not success) and (tries < 3):
        r = requests.get(url)
        success = r.status_code == 200
        tries += 1
        sleep(1)

    if not success:
        print(f'Page {page} does not exist; exit')
        break

    soup = BeautifulSoup(r.text, 'html5lib')

    articles = soup.select('div.articlePreview article div.articlePreview-content a')
    # print(articles)

    contents = []
    for article in articles:
        content = {
            'url': 'https://www.huffingtonpost.fr{}'.format(article['href']),
            'title': normalize('NFKD', article.select_one('h2').text.strip())
        }
        contents.append(content)

    # print (contents)

    with open('exports/huffpost_insolite.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        for content in contents:
            writer.writerow([content['url'], content['title']])

    sleep(1)
    page += 1

    # if page == 3:
        # break
