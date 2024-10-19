from datetime import date, timedelta
from time import sleep
import csv
from bs4 import BeautifulSoup
import requests
# from trafilatura import extract


def get_articles(date, page = None):
    if page is None:
        url = f'https://www.lemonde.fr/archives-du-monde/{date}/'
    else:
        url = f'https://www.lemonde.fr/archives-du-monde/{date}/{page}/'

    print(url)
    r = requests.get(url)
    #print(r.content)

    soup = BeautifulSoup(r.content, 'html5lib')

    articles = soup.select('section#river section.teaser')
    #print(articles)
    for article in articles:
        if (link := article.select_one('a.teaser__link')) and (title := link.select_one('h3.teaser__title')):
            # print(link['href'])
            # print(title.text.strip())
            if link['href'] and title.text:
                with open('exports/le_monde.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([link['href'], title.text.strip()])
            # break

    sleep(1)

    if page is not None:
        return

    pager = soup.select_one('section.river__pagination')

    if not pager:
        return

    page_links = pager.select('a.river__pagination--page')

    if len(page_links) < 2:
        return

    for i in range(2, len(page_links) + 1):
        get_articles(date, i)

today = date.today()

for i in range(90):
    day = today - timedelta(days=i)
    date = day.strftime('%d-%m-%Y')
    print(date)
    get_articles(date)
    print()
    # break
