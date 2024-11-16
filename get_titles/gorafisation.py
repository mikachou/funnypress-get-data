import csv
from time import sleep
from bs4 import BeautifulSoup
import requests
from unicodedata import normalize


page = 1
while (True):
    url = f'https://www.scoop.it/topic/la-gorafisation-du-monde?page={page}'

    print(url)

    tries = 0
    success = False
    while (not success) and (tries < 3):
        r = requests.get(url)
        success = r.status_code == 200
        
        if success:
            soup = BeautifulSoup(r.text, 'html5lib')

            articles = soup.select('article h2.postTitleView a')
            # print(articles)
            
            success = len(articles) > 0

        if not success:
            tries += 1
            sleep(1)

    if not success:
        print(f'Page {page} does not exist; exit')
        break

    contents = []
    for article in articles:

        if inner_h2 := article.select_one('*'):
            inner_h2.decompose()

        content = {
            'url': article['href'],
            'title': normalize('NFKD', article.text.strip())
        }
        contents.append(content)
        # get_page(article['href'])
        # sleep(1)
        # break

    # print (contents)

    with open('exports/gorafisation.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        for content in contents:
            writer.writerow([content['url'], content['title']])

    sleep(1)
    page += 1

    # if page == 3:
        # break
