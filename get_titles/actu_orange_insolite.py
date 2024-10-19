import csv
from bs4 import BeautifulSoup
import requests


url = f'https://actu.orange.fr/societe/insolite/?page=100'

r = requests.get(url)

soup = BeautifulSoup(r.text, 'html5lib')

articles = soup.select('div#showMore a')
# print(articles)

contents = []
for article in articles:
    content = {
        'url': 'https://www.rfi.fr{}'.format(article['href']),
        'title': article.select_one('h2').text.strip()
    }
    contents.append(content)

# print (contents)

with open('exports/actu_orange_insolite.csv', 'a', newline='') as file:
    writer = csv.writer(file)
    for content in contents:
        writer.writerow([content['url'], content['title']])

