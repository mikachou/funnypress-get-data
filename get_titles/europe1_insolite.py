import csv
from time import sleep
from bs4 import BeautifulSoup
import requests
# from unicodedata import normalize


page = 1
while (True):
    if page == 1:
        url = f'https://www.europe1.fr/insolite'
    else:
        url = f'https://www.europe1.fr/insolite/{page}'

    print(url)

    tries = 0
    success = False
    while (not success) and (tries < 3):
        r = requests.get(url)

        soup = BeautifulSoup(r.text, 'html5lib')

        articles = soup.select('ul.block_home_news div.bloc_news a')
        # print(articles)

        success = len(articles) > 0
        tries += 1
        sleep(1)

    if not success:
        print(f'Page {page} does not exist; exit')
        break

    contents = []
    for article in articles:
        if inner_tag := article.select_one('*'):
            inner_tag.decompose()

        content = {
            'url': article['href'],
            'title': article.text.strip()
        }
        contents.append(content)

    # print (contents)

    with open('exports/europe1_insolite.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        for content in contents:
            writer.writerow([content['url'], content['title']])

    sleep(1)
    page += 1

    # if page == 3:
        # break
